from PIL import Image

from src.services.models.BaseModel import BaseModel
from .domains.SpoilerInformation import SpoilerInformation, TextSpoiler, ImageSpoiler, SpoilerElement

import asyncio
import io
import threading
import httpx
import numpy as np

# 모델 인스턴스별 락: 동시 요청이 같은 모델을 여러 스레드에서 동시에 호출하지 않도록 (YOLO 등은 thread-safe 하지 않음)
_model_locks: dict[int, threading.Lock] = {}

async def _predict(model: BaseModel, *args):
    lock = _model_locks.setdefault(id(model), threading.Lock())

    def run():
        with lock:
            return model.predict(*args)

    return await asyncio.to_thread(run)

async def check_spoiler_service(
        video_ids: list[str],
        titles: list[str],
        emotion_recognition: BaseModel,
        ner: BaseModel,
        object_detector: BaseModel,
        pose_detector: BaseModel,
        text_classifier: BaseModel,
        ocr: BaseModel,
) -> list[SpoilerInformation]:
    images = await _fetch_thumbnails(video_ids)

    # OCR -> 텍스트 분석만 순서 의존이 있으므로, 이미지 분석과 병렬 실행
    async def text_pipeline():
        img_arrays = [np.array(img) for img in images]
        ocr_result: list[list[ImageSpoiler]] = await _predict(ocr, img_arrays)
        return await check_text(
            titles,
            ocr_result=ocr_result,
            text_classifier=text_classifier,
            ner=ner,
        )

    (title_spoilers, text_spoilers, ocr_result), image_spoilers = await asyncio.gather(
        text_pipeline(),
        check_image(
            images,
            object_detector=object_detector,
            emotion_recognition=emotion_recognition,
            pose_detector=pose_detector,
        ),
    )

    result = []

    for idx, (spoiler, text_spoiler, image_spoiler) in enumerate(zip(title_spoilers, text_spoilers, image_spoilers)):
        spoiler_information = SpoilerInformation(
            video_id=video_ids[idx],
            title=titles[idx],
            width=images[idx].width,
            height=images[idx].height,
            spoiler=spoiler,
            texts=text_spoiler,
            images=image_spoiler + ocr_result[idx],
        )

        result.append(spoiler_information)

    return result

async def _fetch_thumbnails(video_ids: list[str]) -> list[Image.Image]:
    async with httpx.AsyncClient() as client:
        async def fetch(vid: str) -> Image.Image:
            url = f"https://img.youtube.com/vi/{vid}/mqdefault.jpg"
            resp = await client.get(url)
            resp.raise_for_status()
            return Image.open(io.BytesIO(resp.content)).convert("RGB")

        return list(await asyncio.gather(*(fetch(v) for v in video_ids)))

async def check_image(
        images: list[Image.Image],
        object_detector: BaseModel,
        emotion_recognition: BaseModel,
        pose_detector: BaseModel,
) -> list[list[ImageSpoiler]]:
    # DeepFace가 얼굴 검출까지 알아서 하므로 원본 이미지 전체를 BGR로 배치 호출
    bgr_images = [np.array(img)[:, :, ::-1].copy() for img in images]

    # 이미지 N장을 각각 한 번의 배치 호출로, 세 모델은 병렬 실행
    objects, angles, faces = await asyncio.gather(
        _predict(object_detector, images),       # list[list[det]]
        _predict(pose_detector, images),         # list[list[angle]]
        _predict(emotion_recognition, bgr_images),
    )

    return [
        object + angle + face
        for object, angle, face
        in zip(objects, angles, faces)
    ]

async def check_text(
        titles: list[str],
        text_classifier: BaseModel,
        ner: BaseModel,
        ocr_result: list[list[ImageSpoiler]] | None = None,
) -> tuple[
    list[SpoilerElement],
    list[list[TextSpoiler]],
    list[list[ImageSpoiler]]
]:
    whole_texts: list[str] = []
    title_indices: list[int] = [0]

    # Merging All
    for title, overlay_texts in zip(titles, ocr_result):
        whole_texts += [title] + [overlay_text.label for overlay_text in overlay_texts]
        title_indices.append(len(whole_texts))

    # Text Classification / NER(only applied title) Batch Processing, 병렬 실행
    spoilers, entities = await asyncio.gather(
        _predict(text_classifier, whole_texts),
        _predict(ner, titles),
    )

    title_spoilers: list[SpoilerElement] = [spoilers[_] for _ in title_indices[:-1]]

    overlay_text_spoilers: list[list[SpoilerElement]] = [spoilers[(title_indices[i]+1):title_indices[i+1]] for i in range(len(title_indices)-1)]
    ocr_result: list[list[ImageSpoiler]] = [
        [
            item.set_label(spoiler_element.label)
            .set_confidence(spoiler_element.confidence)
            for item, spoiler_element
            in zip(inner_items, spoiler_elements)
        ] for inner_items, spoiler_elements
        in zip(ocr_result, overlay_text_spoilers)
    ]

    return title_spoilers, entities, ocr_result
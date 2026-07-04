from PIL import Image

from src.services.models.BaseModel import BaseModel
from .domains.SpoilerInformation import SpoilerInformation, TextSpoiler, ImageSpoiler, SpoilerElement

import asyncio
import io
import httpx
import numpy as np

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

    img_arrays = [np.array(img) for img in images]

    ocr_result: list[list[ImageSpoiler]] = ocr.predict(img_arrays)

    title_spoilers, text_spoilers, ocr_result = await check_text(
        titles,
        ocr_result=ocr_result,
        text_classifier=text_classifier,
        ner=ner,
    )

    image_spoilers: list[list[ImageSpoiler]] = await check_image(
        images,
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector,
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
    # 이미지 N장을 각각 한 번의 배치 호출로
    objects: list[list[ImageSpoiler]] = object_detector.predict(images)   # list[list[det]]
    angles: list[list[ImageSpoiler]] = pose_detector.predict(images)         # list[list[angle]]

    # DeepFace가 얼굴 검출까지 알아서 하므로 원본 이미지 전체를 BGR로 배치 호출
    bgr_images = [np.array(img)[:, :, ::-1].copy() for img in images]
    faces: list[list[ImageSpoiler]] = emotion_recognition.predict(bgr_images)

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

    # Text Classification Batch Processing
    spoilers: list[SpoilerElement] = text_classifier.predict(whole_texts)

    # NER Batch Processing, only applied title
    entities: list[list[TextSpoiler]] = ner.predict(titles)

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
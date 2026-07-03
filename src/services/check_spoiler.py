import asyncio
import io
from dataclasses import replace

import httpx
import numpy as np
from PIL import Image

from src.schemas.CheckSpoiler import *
from src.domains.SpoilerInformation import ComplexSpoiler
from src.services.models.BaseModel import BaseModel
from .constants import *


async def batch_check_spoiler_service(
        video_ids: list[str],
        titles: list[str],
        emotion_recognition: BaseModel,
        ner: BaseModel,
        object_detector: BaseModel,
        pose_detector: BaseModel,
        text_classifier: BaseModel,
        ocr: BaseModel,
) -> list[BlurredVideo]:
    # 1. 썸네일 N장 동시 다운로드
    images = await _fetch_thumbnails(video_ids)

    # 2. OCR — 이미지 전체를 한 번의 배치 호출로
    img_arrays = [np.array(img) for img in images]
    ocr_results = ocr.predict(img_arrays)  # list[list[ComplexSpoiler]], 이미지별
    # overlay_texts_per_video[i] = [[ComplexSpoiler, ...]]  (i번째 영상, 이미지 단위 리스트)
    overlay_texts_per_video = [[per_image] for per_image in ocr_results]

    # 3. 텍스트 배치 — 제목 전체 + (제목별 OCR 텍스트) 를 한 번에
    blurred_texts, spoiler_results_per_video = await batch_check_text(
        titles,
        overlay_texts_per_video,
        text_classifier=text_classifier,
        ner=ner,
    )

    # 4. 이미지 배치 — 객체/포즈/감정을 N장 묶어서
    blurred_images = await batch_check_image(
        images,
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector,
    )

    # 5. 영상별로 OCR 결과 + 스포일러 판정 병합
    results = []
    for i, video_id in enumerate(video_ids):
        # spoiler_results_per_video[i] 는 flatten 된 OCR 텍스트 순서와 동일
        flat_overlays = [item for per_image in overlay_texts_per_video[i]
                         for item in per_image]
        merged_overlays: list[ComplexSpoiler] = []
        for ocr_item, entities in zip(flat_overlays,
                                      spoiler_results_per_video[i]):
            if not entities:
                # 스포일러 엔티티 없음 → OCR 결과(label=None) 그대로
                merged_overlays.append(ocr_item)
                continue
            # 엔티티마다 하나씩: bbox/text 는 OCR 영역, label/span/confidence 는 NER 결과
            merged_overlays.extend(
                replace(ocr_item,
                        label=entity.label,
                        confidence=entity.confidence,
                        span=entity.span)
                for entity in entities
            )
        blurred_images[i].overlay_texts = merged_overlays

        results.append(BlurredVideo(
            video_id=video_id,
            blurred_image=blurred_images[i],
            blurred_text=blurred_texts[i],
        ))
    return results


async def _fetch_thumbnails(video_ids: list[str]) -> list[Image.Image]:
    async with httpx.AsyncClient() as client:
        async def fetch(vid: str) -> Image.Image:
            url = f"https://img.youtube.com/vi/{vid}/mqdefault.jpg"
            resp = await client.get(url)
            resp.raise_for_status()
            return Image.open(io.BytesIO(resp.content)).convert("RGB")

        return list(await asyncio.gather(*(fetch(v) for v in video_ids)))


async def batch_check_image(
        images: list[Image.Image],
        object_detector: BaseModel,
        emotion_recognition: BaseModel,
        pose_detector: BaseModel,
) -> list[BlurredImage]:
    # 이미지 N장을 각각 한 번의 배치 호출로
    detections_per_image = object_detector.predict(images)   # list[list[det]]
    angles_per_image = pose_detector.predict(images)         # list[list[angle]]

    # DeepFace가 얼굴 검출까지 알아서 하므로 원본 이미지 전체를 BGR로 배치 호출
    bgr_images = [np.array(img)[:, :, ::-1].copy() for img in images]
    faces_per_image = emotion_recognition.predict(bgr_images)

    results = []
    for i, image in enumerate(images):
        results.append(BlurredImage(
            width=image.width,
            height=image.height,
            objects=detections_per_image[i],
            faces=faces_per_image[i],
            angles=angles_per_image[i],
            overlay_texts=None,
        ))
    return results


async def batch_check_text(
        titles: list[str],
        overlay_texts_per_video: list[list],
        text_classifier: BaseModel,
        ner: BaseModel,
) -> tuple[list[BlurredText], list[list]]:
    # --- 제목 분류: N개 제목을 한 번에 ---
    spoilers = text_classifier.predict(titles)   # list[SpoilerElement], 제목별 분류 결과

    # --- NER: 제목 + OCR 텍스트 전부를 flatten해서 한 번에 ---
    flat_texts: list[str] = []
    ocr_counts: list[int] = []   # 영상별 OCR 텍스트 수 (unflatten용)
    for title, overlays in zip(titles, overlay_texts_per_video):
        flat_texts.append(title)
        ocr_texts = [item.text for per_image in overlays for item in per_image]
        flat_texts.extend(ocr_texts)
        ocr_counts.append(len(ocr_texts))

    all_entities = ner.predict(flat_texts)   # flat_texts와 같은 길이

    # --- unflatten: [제목, ocr*n] 블록 단위로 다시 나눔 ---
    blurred_texts: list[BlurredText] = []
    spoiler_results_per_video: list[list] = []
    cursor = 0
    for i, title in enumerate(titles):
        title_entities = all_entities[cursor]
        ocr_entities = all_entities[cursor + 1: cursor + 1 + ocr_counts[i]]
        cursor += 1 + ocr_counts[i]

        blurred_texts.append(BlurredText.from_entities(
            text=title,
            spoiler=spoilers[i],
            entities=title_entities,
            level_map=ENTITY_TO_SPOILER_LEVEL,
        ))
        spoiler_results_per_video.append(ocr_entities)

    return blurred_texts, spoiler_results_per_video


# src.api.v1.endpoints.check_spoiler 에서 import 하는 이름
check_spoiler_service = batch_check_spoiler_service
from PIL import Image

from src.schemas.CheckSpoiler import *
from src.services.models.BaseModel import BaseModel

from .constants import *

import httpx
import numpy as np
import io

async def check_spoiler_service(
        video_id: str,
        title: str,
        emotion_recognition: BaseModel,
        ner: BaseModel,
        object_detector: BaseModel,
        pose_detector: BaseModel,
        text_classifier: BaseModel,
        ocr: BaseModel,
) -> BlurredVideo:
    image_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"

    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        response.raise_for_status()

    image = Image.open(io.BytesIO(response.content)).convert('RGB')
    img_array = np.array(image)

    overlay_texts = ocr.extract(img_array)
    texts = [title] + [_[1] for _ in overlay_texts]

    blurred_title, text_spoiler_results = await check_text(
        texts,
        text_classifier=text_classifier,
        ner=ner
    )

    blurred_image = await check_image(
        image,
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector
    )

    blurred_image.overlay_texts = overlay_texts

    merged_overlays = []
    for ocr_item, spoiler_info in zip(overlay_texts, text_spoiler_results):
        bbox, text, confidence = ocr_item
        merged_overlays.append({
            "box": [[int(x), int(y)] for x, y in bbox],
            "text": str(text),
            "ocr_confidence": float(confidence),
            "spoiler": spoiler_info,
        })

    return BlurredVideo(
        video_id=video_id,
        blurred_image=blurred_image,
        blurred_text=blurred_title,
    )

async def check_image(
        image: Image.Image,
        object_detector: BaseModel,
        emotion_recognition: BaseModel,
        pose_detector: BaseModel,
) -> BlurredImage:
    detections = object_detector.extract(image)
    angles = pose_detector.extract(image)

    objects = []  # objects without facial
    faces = []
    bgr_faces = [] # cropped facial images that inputting into DeepFace

    for det in detections:
        if "face" not in det["label"]:
            objects.append(det)
            continue
        x0, y0, x1, y1 = map(int, det["box"])
        crop = image.crop((x0, y0, x1, y1))
        faces.append(det)    # box·confidence·label
        bgr_faces.append(np.array(crop)[:, :, ::-1])

    emotions = emotion_recognition.extract(bgr_faces)

    face_results = [
        {**face, **emotion}
        for face, emotion in zip(faces, emotions)
    ]

    return BlurredImage(
        width=image.width,
        height=image.height,
        objects=objects,
        faces=face_results,
        angles=angles,
        overlay_texts=None
    )

async def check_text(
        texts: list[str],
        text_classifier: BaseModel,
        ner: BaseModel
) -> tuple[BlurredText, list]:
    # For Title
    spoiler: str = text_classifier.extract(texts[0])

    entities = ner.extract(texts)

    result = dict()
    for label in entities[0]['entities'].keys():
        spoiler_level = ENTITY_TO_SPOILER_LEVEL[label]
        spans = result.get(spoiler_level, [])

        for entity in entities[0]['entities'][label]:
            spans.append(Span(
                text=entity["text"],
                confidence=entity["confidence"],
                start=entity["start"],
                end=entity["end"]
            ))

        result[spoiler_level] = spans

    return BlurredText(
        text = texts[0],
        spoiler = spoiler,
        spans = result
    ), entities[1:]
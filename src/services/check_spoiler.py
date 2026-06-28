from PIL import Image

from src.schemas.CheckSpoiler import *
from src.services.constants import *

import numpy as np
import requests

async def check_spoiler_service(
        video_id: str,
        title: str,
        emotion_recognition: BaseModel,
        ner: BaseModel,
        object_detector: BaseModel,
        pose_detector: BaseModel,
        text_classifier: BaseModel
) -> BlurredVideo:
    image_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')

    blurred_image = await check_image(
        image,
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector
    )

    blurred_text = await check_text(
        title,
        text_classifier=text_classifier,
        ner=ner
    )

    return BlurredVideo(
        video_id=video_id,
        blurred_image=blurred_image,
        blurred_text=blurred_text
    )

async def check_image(
        image: Image.Image,
        object_detector: BaseModel,
        emotion_recognition: BaseModel,
        pose_detector: BaseModel,
) -> BlurredImage:
    detections = object_detector.extract(image)
    angles = pose_detector.extract(image)

    objects = []  # face가 아닌 것들만 남김
    faces = []
    bgr_faces = [] # emotion 모델 입력용 crop

    for det in detections:
        if "face" not in det["label"]:
            objects.append(det)
            continue
        x0, y0, x1, y1 = map(int, det["box"])
        crop = image.crop((x0, y0, x1, y1))
        faces.append(det)    # box·confidence·label 그대로 보관
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
    )

async def check_text(
        text: str,
        text_classifier: BaseModel,
        ner: BaseModel
) -> BlurredText:
    spoiler: str = text_classifier.extract(text)

    entities = ner.extract(text)

    result = dict()
    for label in entities['entities'].keys():
        spoiler_level = ENTITY_TO_SPOILER_LEVEL[label]
        spans = result.get(spoiler_level, [])

        for entity in entities['entities'][label]:

            # TODO: Add business logic for Hiding ex. scoring_text + name

            spans.append(Span(
                text=entity["text"],
                confidence=entity["confidence"],
                start=entity["start"],
                end=entity["end"]
            ))

        result[spoiler_level] = spans

    return BlurredText(
        text = text,
        spoiler = spoiler,
        spans = result
    )
from PIL import Image

from src.services.check_spoiler import check_text, check_image, check_spoiler_service
from src.services.models.EmotionRecognition import DeepFaceRecognition
from src.services.models.NER import GliNER
from src.services.models.ObjectDetector import GroundingDINO
from src.services.models.PoseDetector import YoloV8Pose
from src.services.models.TextClassifier import SetFitImpl
from tests.services.constants import *

import requests
import asyncio

from tests.utils import prettier

def test_check_spoiler_service():
    object_detector = GroundingDINO()
    emotion_recognition = DeepFaceRecognition()
    pose_detector = YoloV8Pose()
    text_classifier = SetFitImpl()
    ner = GliNER()

    video_id = VIDEO_ID_EX
    title = TITLE_EX

    result = asyncio.run(check_spoiler_service(
        video_id,
        title,
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector,
        text_classifier=text_classifier,
        ner=ner
    ))

    prettier(result)

def test_check_text():
    text_classifier = SetFitImpl()
    ner = GliNER()

    result = asyncio.run(check_text(
        TITLE_EX,
        text_classifier,
        ner
    ))

    prettier(result)

def test_check_image():
    image = Image.open(requests.get(IMAGE_URL, stream=True).raw).convert("RGB")

    object_detector = GroundingDINO()
    emotion_recognition = DeepFaceRecognition()
    pose_detector = YoloV8Pose()

    result = asyncio.run(check_image(
        image,
        object_detector,
        emotion_recognition,
        pose_detector
    ))

    prettier(result)
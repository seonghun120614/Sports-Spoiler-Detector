from src.services.spoiler_services import *
from src.services.models.OCR import EasyOCR
from src.services.models.EmotionRecognition import DeepFaceRecognition
from src.services.models.NER import GliNER
from src.services.models.ObjectDetector import GroundingDINO
from src.services.models.PoseDetector import YoloV26Pose
from .constants import *

import requests
import asyncio

def test_batch_check_spoiler_service():
    object_detector = GroundingDINO()
    emotion_recognition = DeepFaceRecognition()
    pose_detector = YoloV26Pose()
    ner = GliNER()
    ocr = EasyOCR()

    video_id = VIDEO_ID_EX

    result = asyncio.run(check_spoiler_service(
        [video_id],
        [TITLE_EX],
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector,
        ner=ner,
        ocr=ocr
    ))

def test_batch_check_text():
    ner = GliNER()

    result = asyncio.run(check_text([TITLE_EX], ner=ner))

def test_batch_check_image():
    image = Image.open(requests.get(IMAGE_URL_EX, stream=True).raw).convert("RGB")

    object_detector = GroundingDINO()
    emotion_recognition = DeepFaceRecognition()
    pose_detector = YoloV26Pose()

    result = asyncio.run(batch_check_image(
        [image],
        object_detector,
        emotion_recognition,
        pose_detector
    ))
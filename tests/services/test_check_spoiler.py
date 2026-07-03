from src.domains.SpoilerInformation import ComplexSpoiler, BoundingBox, Point
from src.services.check_spoiler import *
from src.services.models.OCR import EasyOCR
from src.services.models.EmotionRecognition import DeepFaceRecognition
from src.services.models.NER import GliNER
from src.services.models.ObjectDetector import GroundingDINO
from src.services.models.PoseDetector import YoloV26Pose
from src.services.models.TextClassifier import SetFitImpl
from .constants import *

import requests
import asyncio

def test_batch_check_spoiler_service():
    object_detector = GroundingDINO()
    emotion_recognition = DeepFaceRecognition()
    pose_detector = YoloV26Pose()
    text_classifier = SetFitImpl()
    ner = GliNER()
    ocr = EasyOCR()

    video_id = VIDEO_ID_EX

    result = asyncio.run(batch_check_spoiler_service(
        [video_id],
        [TITLE_EX],
        object_detector=object_detector,
        emotion_recognition=emotion_recognition,
        pose_detector=pose_detector,
        text_classifier=text_classifier,
        ner=ner,
        ocr=ocr
    ))

def test_batch_check_text():
    text_classifier = SetFitImpl()
    ner = GliNER()

    mock_overlay = ComplexSpoiler(
        label=None, confidence=0.99, text="2:1",
        bounding_box=BoundingBox(top_left=Point(x=13, y=39),
                                 bottom_right=Point(x=129, y=99)),
        span=None,
    )

    result = asyncio.run(batch_check_text(
        [TITLE_EX],
        [[[mock_overlay]]],  # 실제 OCR 출력과 동일한 3겹 구조
        text_classifier, ner,
    ))

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
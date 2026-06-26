# 실행:
from PIL import Image

from src.services.models.EmotionRecognition import DeepFaceRecognition
from src.services.models.ObjectDetector import GroundingDINO

from tests.services.constants import *

import numpy as np
import requests


def test_deepface():
    image = Image.open(requests.get(IMAGE_URL, stream=True).raw).convert("RGB")

    detector = GroundingDINO()
    objects = detector.extract(image, threshold=0.3)

    face_boxes = []
    bgr_faces = []
    for object in objects:
        if not "face" in object["label"]: continue

        x0, y0, x1, y1 = map(int, object["box"])
        face = image.crop((x0, y0, x1, y1))
        face_boxes.append([x0, y0, x1, y1])
        bgr_faces.append(np.array(face)[:, :, ::-1])

    recognizer = DeepFaceRecognition()
    results = recognizer.extract(bgr_faces)

    print(results)
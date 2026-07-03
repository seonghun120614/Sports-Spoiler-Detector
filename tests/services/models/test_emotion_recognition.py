# 실행: uv run pytest tests/services/models/test_emotion_recognition.py -s
import numpy as np
from PIL import Image

from src.services.models.EmotionRecognition import DeepFaceRecognition

from tests.services.constants import *

import requests


def test_deepface():
    image = Image.open(requests.get(IMAGE_URL_EX, stream=True).raw).convert("RGB")

    recognizer = DeepFaceRecognition()
    results = recognizer.predict([np.array(image)])

    print(results)
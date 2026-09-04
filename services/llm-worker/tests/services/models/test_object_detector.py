# 실행: uv run pytest tests/test_object_detector.py -s
import requests

from PIL import Image

from src.services.models.ObjectDetector import GroundingDINO

from tests.services.constants import *


def test_grounding_dino():
    detector = GroundingDINO()

    img = Image.open(requests.get(IMAGE_URL_EX, stream=True).raw).convert("RGB")

    results = detector.predict([img], threshold=0.3)

    print(results)
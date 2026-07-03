# 실행: uv run pytest tests/test_pose_detector.py -s
import requests
from PIL import Image

from src.services.models.PoseDetector import YoloV26Pose
from tests.services.constants import *


def test_yolov26pose():
    model = YoloV26Pose()

    img = Image.open(requests.get(IMAGE_URL_EX, stream=True).raw).convert("RGB")

    results = model.predict([img])

    print(results)
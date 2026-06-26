# 실행: uv run pytest tests/test_pose_detector.py -s
import requests
from PIL import Image

from src.services.models.PoseDetector import YoloV8Pose
from tests.services.constants import *


def test_yolov8pose():
    model = YoloV8Pose()

    results = model.extract(Image.open(requests.get(IMAGE_URL, stream=True).raw).convert("RGB"), debug=False)

    print(results)
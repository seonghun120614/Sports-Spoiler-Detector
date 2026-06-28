# 실행: uv run pytest tests/test_object_detector.py -s
import requests

from PIL import Image

from src.services.models.ObjectDetector import GroundingDINO

from tests.services.constants import *

from collections import defaultdict


def pretty_print(detections):
    grouped = defaultdict(list)
    for d in detections:
        grouped[d["label"]].append(d)

    print(f"\n감지된 객체: {len(detections)}개")
    for label, items in grouped.items():
        print(f"\n[{label}] {len(items)}개")
        for d in sorted(items, key=lambda x: x["confidence"], reverse=True):
            x0, y0, x1, y1 = (round(v, 1) for v in d["box"])
            print(f"  conf={d['confidence']:.3f}  box=({x0}, {y0}, {x1}, {y1})")

def test_grounding_dino():
    detector = GroundingDINO()

    results = detector.extract(Image.open(requests.get(IMAGE_URL, stream=True).raw), threshold=0.3)
    print()
    print(results)
    print()
    print("================")

    pretty_print(results)
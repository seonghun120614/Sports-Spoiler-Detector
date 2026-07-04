from contextlib import asynccontextmanager

from fastapi import FastAPI

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if "TEST_FLAG" not in os.environ:
        from src.services.models import (
            GliNER, GroundingDINO, SetFitImpl,
            DeepFaceRecognition, YoloV26Pose,
            EasyOCR)
        try:
            app.state.models = {
                "ocr": EasyOCR(),
                "ner": GliNER(),
                "object_detector": GroundingDINO(),
                "text_classifier": SetFitImpl(),
                "emotion_recognition": DeepFaceRecognition(),
                "pose_detector": YoloV26Pose(),
            }
        except Exception as e:
            print(f"[lifespan] 모델 로딩 실패: {e}")
            import traceback
            traceback.print_exc()
            app.state.models.clear()
            os.environ["TEST_FLAG"] = "1"
    yield
    app.state.models.clear()
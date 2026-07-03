from contextlib import asynccontextmanager

from fastapi import FastAPI

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    if "TEST_FLAG" not in os.environ:
        from src.services.models import (
            GliNER, GroundingDINO, SetFitImpl,
            DeepFaceRecognition, YoloV8Pose,
            EasyOCR
        )
        try:
            app.state.ocr = EasyOCR()
            app.state.ner = GliNER()
            app.state.object_detector = GroundingDINO()
            app.state.text_classifier = SetFitImpl()
            app.state.emotion_recognition = DeepFaceRecognition()
            app.state.pose_detector = YoloV8Pose()
        except Exception:
            print("")
            for attr in ("ner", "object_detector", "text_classifier",
                         "emotion_recognition", "pose_detector"):
                if hasattr(app.state, attr):
                    delattr(app.state, attr)
            os.environ["TEST_FLAG"] = "1"

    yield
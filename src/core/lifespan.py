from contextlib import asynccontextmanager

from fastapi import FastAPI, logger

from src.services.models import *

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.ner = GliNER()
        app.state.object_detector = GroundingDINO()
        app.state.text_classifier = SetFitImpl()
        app.state.emotion_recognition = DeepFaceRecognition()
        app.state.pose_detector = YoloV8Pose()
    except Exception as e:
        logger.error("모델 로딩 실패 — TEST 모드로 전환합니다")
        os.environ["TEST_FLAG"] = "1"
    yield
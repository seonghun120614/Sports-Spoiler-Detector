from contextlib import asynccontextmanager

from fastapi import FastAPI, logger

from src.services.models import *

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not "TEST_FLAG" in os.environ:
        app.state.ner = GliNER()
        app.state.object_detector = GroundingDINO()
        app.state.text_classifier = SetFitImpl()
        app.state.emotion_recognition = DeepFaceRecognition()
        app.state.pose_detector = YoloV8Pose()

    logger.error("[TEST 모드]")
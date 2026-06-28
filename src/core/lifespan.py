from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.services.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ner = GliNER()
    app.state.object_detector = GroundingDINO()
    app.state.text_classifier = SetFitImpl()
    app.state.emotion_recognition = DeepFaceRecognition()
    app.state.pose_detector = YoloV8Pose()
    yield
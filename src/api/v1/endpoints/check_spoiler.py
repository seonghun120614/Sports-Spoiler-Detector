from datetime import datetime
from fastapi import APIRouter, Request

from src.schemas.CheckSpoiler import CheckSpoilerRequest, CheckSpoilerResponse
from src.services.check_spoiler import check_spoiler_service
from .constants import _TEST_RESPONSE_DATA

import os

router = APIRouter(prefix="/v1", tags=["Spoiler"])

@router.post("/check-spoiler")
async def check_spoiler(
        request: Request,
        body: list[CheckSpoilerRequest]
) -> list[CheckSpoilerResponse]:
    video_ids = [_.video_id for _ in body]
    titles = [_.title for _ in body]

    if body is None:
        return []

    if "TEST_FLAG" in os.environ:
        return [CheckSpoilerResponse.model_validate(_TEST_RESPONSE_DATA)]

    blurred_videos = await check_spoiler_service(
        video_ids,
        titles,
        object_detector=request.app.state.object_detector,
        pose_detector=request.app.state.pose_detector,
        ner=request.app.state.ner,
        text_classifier=request.app.state.text_classifier,
        emotion_recognition=request.app.state.emotion_recognition,
        ocr=request.app.state.ocr,
    )

    return [CheckSpoilerResponse(
        blurred_video=blurred_video,
        timestamp=datetime.now()
    ) for blurred_video in blurred_videos]
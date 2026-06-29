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
        body: CheckSpoilerRequest
) -> CheckSpoilerResponse:
    video_id = body.video_id
    title = body.title

    if video_id is None or len(video_id) != 11 or title is None or len(title) <= 1:
        return CheckSpoilerResponse(blurred_video=None)

    if "TEST_FLAG" in os.environ:
        return CheckSpoilerResponse.model_validate(_TEST_RESPONSE_DATA)

    blurred_video = await check_spoiler_service(
        video_id,
        title,
        object_detector=request.app.state.object_detector,
        pose_detector=request.app.state.pose_detector,
        ner=request.app.state.ner,
        text_classifier=request.app.state.text_classifier,
        emotion_recognition=request.app.state.emotion_recognition,
    )

    return CheckSpoilerResponse(
        blurred_video=blurred_video,
        timestamp=datetime.now()
    )
from typing import Any
from fastapi import APIRouter, Request

from src.services.domains.SpoilerInformation import SpoilerInformation
from src.services.spoiler_services import check_spoiler_service
from .constants import _TEST_RESPONSE_DATA
from ..schemas.Responses import CheckSpoilerResponse
from ..schemas.Requests import CheckSpoilerRequest

import os

router = APIRouter(prefix="/v1", tags=["Spoiler"])

@router.post("/check-spoiler", response_model=CheckSpoilerResponse)
async def check_spoiler(
        request: Request,
        body: list[CheckSpoilerRequest]
) -> Any:
    if not body: return []
    if "TEST_FLAG" in os.environ:
        return [CheckSpoilerResponse.model_validate(_TEST_RESPONSE_DATA)]

    video_ids = [_.video_id for _ in body]
    titles = [_.title for _ in body]

    spoiler_information: list[SpoilerInformation] = await check_spoiler_service(
        video_ids,
        titles,
        **request.app.state.models
    )

    return CheckSpoilerResponse.from_domain(spoiler_information)
from typing import Sequence
from pydantic import BaseModel, Field
from datetime import datetime

from src.services.domains.SpoilerInformation import SpoilerInformation

class CheckSpoilerResponse(BaseModel):
    spoiler_information: dict[str, SpoilerInformation]
    api_version: str = "v1"
    timestamp: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_domain(cls,
                   spoiler_information: Sequence[SpoilerInformation]
                   ) -> "CheckSpoilerResponse":
        return cls(
            spoiler_information={
                _.video_id : _
                for _ in spoiler_information
            }
        )
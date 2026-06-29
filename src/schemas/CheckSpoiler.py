from datetime import datetime

from pydantic import BaseModel

class CheckSpoilerRequest(BaseModel):
    video_id: str
    title: str

# ===== For Image ======
class BlurredImage(BaseModel):
    width: int
    height: int
    objects: list | dict
    faces: list | dict
    angles: list | dict

# ===== For Text =====
class Span(BaseModel):
    text: str
    confidence: float
    start: int
    end: int

class BlurredText(BaseModel):
    text: str
    spoiler: str
    spans: dict[int, list[Span]]

# ===== For Service =====
class BlurredVideo(BaseModel):
    video_id: str
    blurred_image: BlurredImage
    blurred_text: BlurredText

# ===== For Response =====
class CheckSpoilerResponse(BaseModel):
    blurred_video: BlurredVideo | None
    timestamp: datetime = datetime.now()
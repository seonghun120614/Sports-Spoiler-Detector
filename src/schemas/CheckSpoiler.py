from collections import defaultdict
from datetime import datetime
from typing import Mapping, Sequence

from pydantic import BaseModel, Field

from src.domains.SpoilerInformation import SpoilerElement, TextSpoiler

class CheckSpoilerRequest(BaseModel):
    video_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{11}$")
    title: str = Field(..., min_length=1)

# ===== For Image ======
class BlurredImage(BaseModel):
    width: int
    height: int
    objects: list | dict
    faces: list | dict
    angles: list | dict
    overlay_texts: list | dict | None

# ===== For Text =====
class Span(BaseModel):
    label: str | None = None
    text: str
    confidence: float
    start: int
    end: int

    @classmethod
    def from_entity(cls, entity: TextSpoiler) -> "Span":
        return cls(
            label=entity.label,
            text=entity.text,
            confidence=entity.confidence,
            start=entity.span.start,
            end=entity.span.end,
        )

class BlurredText(BaseModel):
    text: str
    spoiler: str
    spans: dict[int, list[Span]]

    @classmethod
    def from_entities(cls,
                      text: str,
                      spoiler: SpoilerElement,
                      entities: Sequence[TextSpoiler],
                      level_map: Mapping[str, int],
                      ) -> "BlurredText":
        """NER 엔티티(domain)를 스포일러 레벨별 Span으로 묶어 생성"""
        spans: dict[int, list[Span]] = defaultdict(list)
        for entity in entities:
            spans[level_map[entity.label]].append(Span.from_entity(entity))
        return cls(text=text, spoiler=spoiler.label, spans=dict(spans))

# ===== For Service =====
class BlurredVideo(BaseModel):
    video_id: str
    blurred_image: BlurredImage
    blurred_text: BlurredText

# ===== For Response =====
class CheckSpoilerResponse(BaseModel):
    blurred_video: BlurredVideo | None
    timestamp: datetime = datetime.now()
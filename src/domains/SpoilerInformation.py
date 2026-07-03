from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import Sequence

@dataclass(frozen=True, kw_only=True)
class Point:
    x: int | float
    y: int | float

    def copy(self, **changes) -> "Point":
        return replace(self, **changes)


@dataclass(frozen=True, kw_only=True)
class BoundingBox:
    top_left: Point
    bottom_right: Point

    def xyxy(self) -> tuple[int, int, int, int]:
        return self.top_left.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y


@dataclass(frozen=True, kw_only=True)
class SpoilerElement:
    label: str
    confidence: float


@dataclass(frozen=True, kw_only=True)
class TextSpan:
    start: int
    end: int


@dataclass(frozen=True, kw_only=True)
class TextSpoiler(SpoilerElement):
    text: str
    span: TextSpan

    @classmethod
    def create(cls,
               spoiler_elem: SpoilerElement,
               text_span: TextSpan,
               text: str
               ) -> "TextSpoiler":
        return TextSpoiler(label=spoiler_elem.label,
                           confidence=spoiler_elem.confidence,
                           span=text_span, text=text)


@dataclass(frozen=True, kw_only=True)
class ImageSpoiler(SpoilerElement):
    bounding_box: BoundingBox

    @classmethod
    def create(cls,
               spoiler_elem: SpoilerElement,
               bounding_box: BoundingBox
               ) -> "ImageSpoiler":
        return ImageSpoiler(label=spoiler_elem.label,
                            confidence=spoiler_elem.confidence,
                            bounding_box=bounding_box)

@dataclass(frozen=True, kw_only=True)
class ComplexSpoiler(SpoilerElement):
    label: str | None
    text: str
    bounding_box: BoundingBox
    span: TextSpan | None = field(default=None)

@dataclass(frozen=True, kw_only=True)
class SpoilerInformation:
    video_id: str
    width: int
    height: int
    texts: Sequence[TextSpoiler]
    images: Sequence[ImageSpoiler]
    overlay_texts: Sequence[ComplexSpoiler]
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def total_spoiler_count(self) -> int:
        return len(self.texts) + len(self.images) + len(self.overlay_texts)

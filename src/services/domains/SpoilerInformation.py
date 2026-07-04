from dataclasses import dataclass, replace
from typing import Sequence

@dataclass(frozen=True, kw_only=True)
class Point:
    x: int | float
    y: int | float

    def copy(self, **changes) -> "Point":
        return replace(self, **changes)

    def scaling(self, multiplier_x: float, multiplier_y: float) -> "Point":
        return replace(self, x=self.x * multiplier_x, y=self.y * multiplier_y)

@dataclass(frozen=True, kw_only=True)
class BoundingBox:
    top_left: Point
    bottom_right: Point

    def xyxy(self) -> tuple[int, int, int, int]:
        return self.top_left.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y

@dataclass(frozen=True, kw_only=True)
class SpoilerElement:
    label: str | None = None
    confidence: float

@dataclass(frozen=True, kw_only=True)
class TextSpan:
    start: int
    end: int

@dataclass(frozen=True, kw_only=True)
class TextSpoiler(SpoilerElement):
    label: str | None = None
    text: str
    span: TextSpan

    @classmethod
    def create(cls,
               spoiler_elem: SpoilerElement,
               text_span: TextSpan,
               text: str,
               label: str | None = None,
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
        return cls(label=spoiler_elem.label,
                            confidence=spoiler_elem.confidence,
                            bounding_box=bounding_box)

    def set_label(self, label: str) -> "ImageSpoiler":
        return replace(self, label=label)

@dataclass(frozen=True, kw_only=True)
class SpoilerInformation:
    video_id: str
    title: str
    width: int
    height: int
    spoiler: str
    texts: Sequence[TextSpoiler]
    images: Sequence[ImageSpoiler]

    @property
    def total_spoiler_count(self) -> int:
        return len(self.texts) + len(self.images) + len(self.overlay_texts)

from src.domains.SpoilerInformation import ComplexSpoiler, Point, BoundingBox
from src.services.models.BaseModel import BaseModel

import numpy as np

_TARGET_WIDTH = 640
_TARGET_HEIGHT = 360

class EasyOCR(BaseModel):
    def __init__(self):
        import easyocr
        self._reader = easyocr.Reader(['en', 'ko'])

    def predict(self, images: list[np.ndarray]) -> list[list[ComplexSpoiler]]:
        if not images: return []

        original_sizes = [(img.shape[0], img.shape[1]) for img in images]


        results = self._reader.readtext_batched(
            images,
            n_width=_TARGET_WIDTH,
            n_height=_TARGET_HEIGHT,
        )

        output = []
        for raw, (orig_h, orig_w) in zip(results, original_sizes):
            scale_x = orig_w / _TARGET_WIDTH
            scale_y = orig_h / _TARGET_HEIGHT

            one = []
            for bbox, text, conf in raw:
                # bbox: [top_left, top_right, bottom_right, bottom_left], 각 [x, y]
                # 회전된 텍스트도 안전하게 min/max로 축정렬 박스 계산
                xs = [pt[0] for pt in bbox]
                ys = [pt[1] for pt in bbox]

                # 4. 원본 크기로 되돌리기 (스케일 곱) + 경계 클램프
                left = int(min(xs) * scale_x)
                top = int(min(ys) * scale_y)
                right = int(max(xs) * scale_x)
                bottom = int(max(ys) * scale_y)

                left = max(0, min(left, orig_w))
                right = max(0, min(right, orig_w))
                top = max(0, min(top, orig_h))
                bottom = max(0, min(bottom, orig_h))

                top_left = Point(x=left, y=top)
                bottom_right = Point(x=right, y=bottom)

                one.append(
                    ComplexSpoiler(
                        label=None,
                        confidence=round(float(conf), 2),
                        text=str(text),
                        bounding_box=BoundingBox(
                            top_left=top_left,
                            bottom_right=bottom_right,
                        ),
                        span=None,
                    )
                )
            output.append(one)
        return output
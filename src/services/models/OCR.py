from src.domains.SpoilerInformation import ComplexSpoiler, Point, BoundingBox
from src.services.models.BaseModel import BaseModel

import numpy as np

class EasyOCR(BaseModel):
    def __init__(self):
        import easyocr
        self._reader = easyocr.Reader(['en', 'ko'])

    def predict(self, images: list[np.ndarray]) -> list[list[ComplexSpoiler]]:
        results = self._reader.readtext_batched(images)

        output = []
        for raw in results:  # 이미지별
            one = []
            for bbox, text, conf in raw:
                top_left = Point(x=int(bbox[0][0]), y=int(bbox[0][1]))
                bottom_right = Point(x=int(bbox[2][0]), y=int(bbox[2][1]))
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
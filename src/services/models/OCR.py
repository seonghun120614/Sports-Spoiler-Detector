from src.services.domains.SpoilerInformation import Point, BoundingBox, ImageSpoiler
from src.services.models.BaseModel import BaseModel

import numpy as np

from src.services.models.constants import THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, OCR_LANG


class EasyOCR(BaseModel):
    def __init__(self):
        import easyocr
        self._reader = easyocr.Reader(OCR_LANG)

    def predict(self, images: list[np.ndarray]) -> list[list[ImageSpoiler]]:
        if not images: return []

        # Saving original sizes
        original_sizes = [(img.shape[0], img.shape[1]) for img in images]

        # Inference with consistence size
        results = self._reader.readtext_batched(
            images,
            n_width=THUMBNAIL_WIDTH,
            n_height=THUMBNAIL_HEIGHT,
        )

        output = []
        for raw, (orig_h, orig_w) in zip(results, original_sizes):
            # Calc. multiplier
            scale_x = orig_w / THUMBNAIL_WIDTH
            scale_y = orig_h / THUMBNAIL_HEIGHT

            one = []
            for bbox, text, conf in raw:
                # bbox: [top_left, top_right, bottom_right, bottom_left]
                top_left, bottom_right = bbox[0], bbox[2]

                top_left = Point(x=top_left[0], y=top_left[1]).scaling(scale_x, scale_y)
                bottom_right = Point(x=bottom_right[0], y=bottom_right[1]).scaling(scale_x, scale_y)

                one.append(
                    ImageSpoiler(
                        label=text,
                        confidence=round(float(conf), 2),
                        bounding_box=BoundingBox(
                            top_left=top_left,
                            bottom_right=bottom_right,
                        ),
                    )
                )
            output.append(one)
        return output
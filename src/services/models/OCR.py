from src.services.models.BaseModel import BaseModel

import numpy as np

class EasyOCR(BaseModel):
    def __init__(self):
        import easyocr
        self._reader = easyocr.Reader(['en', 'ko'])

    def predict(self, image: np.ndarray) -> list:
        raw = self._reader.readtext(image)
        return [
            (
                [[int(x), int(y)] for x, y in bbox],
                str(text),
                float(conf),
            )
            for bbox, text, conf in raw
        ]

    def batch_predict(self, arg):
        pass
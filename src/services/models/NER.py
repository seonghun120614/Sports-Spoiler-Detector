from src.services.models.BaseModel import BaseModel

from dataclasses import dataclass

from .constants import *

import numpy as np

def _clean_numpy(obj):
    """numpy 타입을 파이썬 기본 타입으로 재귀 변환"""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: _clean_numpy(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean_numpy(v) for v in obj]
    return obj


@dataclass
class GliNER(BaseModel):
    def __post_init__(self):
        from gliner2 import GLiNER2
        self._model = GLiNER2.from_pretrained(
            NER_MODEL_PATH,
            map_location=DEVICE,
        )
        self._model.eval()

    def predict(self, texts: list[str], threshold: float = 0.5):
        result = self._model.batch_extract_entities(
            texts,
            entity_types=ENTITY_DESC,
            threshold=threshold,
            include_confidence=True,
            include_spans=True,
        )
        return _clean_numpy(result)

    def batch_predict(self, texts: list[str], threshold: float = 0.5):
        pass
from src.services.models.BaseModel import BaseModel

from dataclasses import dataclass

from .constants import *

@dataclass
class GliNER(BaseModel):
    def __post_init__(self):
        from gliner2 import GLiNER2
        self._model = GLiNER2.from_pretrained(
            NER_MODEL_PATH,
            map_location=DEVICE,
        )
        self._model.eval()

    def extract(self, text: str, threshold: float = 0.5):
        return self._model.extract_entities(
            text,
            entity_types=ENTITY_DESC,
            threshold=threshold,
            include_confidence=True,
            include_spans=True,
        )
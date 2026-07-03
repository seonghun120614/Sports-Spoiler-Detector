from src.services.models.BaseModel import BaseModel

from dataclasses import dataclass

from .constants import *
from ...domains.SpoilerInformation import SpoilerElement, TextSpan, TextSpoiler


@dataclass
class GliNER(BaseModel):
    def __post_init__(self):
        from gliner2 import GLiNER2
        self._model = GLiNER2.from_pretrained(
            NER_MODEL_PATH,
            map_location=DEVICE,
        )
        self._model.eval()

    def predict(self, texts: list[str], threshold: float = 0.5) -> list[list[TextSpoiler]]:
        result = []
        outputs = self._model.batch_extract_entities(
            texts,
            entity_types=ENTITY_DESC,
            threshold=threshold,
            include_confidence=True,
            include_spans=True,
        )
        for text in outputs:
            one = []
            for label, entities in text['entities'].items():
                for entity in entities:
                    spoiler_elem = SpoilerElement(label=label, confidence=entity['confidence'])
                    text_span = TextSpan(start=entity['start'], end=entity['end'])
                    text_spoiler = TextSpoiler.create(spoiler_elem=spoiler_elem,
                                                      text_span=text_span,
                                                      text=entity['text'])
                    one.append(text_spoiler)
            result.append(one)
        return result

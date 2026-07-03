import transformers.training_args
from transformers.integrations.integration_utils import default_logdir as _default_logdir
if not hasattr(transformers.training_args, "default_logdir"):
    transformers.training_args.default_logdir = _default_logdir
from dataclasses import dataclass

from src.domains.SpoilerInformation import SpoilerElement
from src.services.models.BaseModel import BaseModel
from .constants import *

@dataclass
class SetFitImpl(BaseModel):
    def __post_init__(self):
        from setfit import SetFitModel
        self._model = SetFitModel.from_pretrained(
            SETFIT_MODEL_PATH,
            labels=["Direct Spoiler", "Indirect Spoiler", "Non-Spoiler"],
        )

    def predict(self, inputs: list[str]) -> list[SpoilerElement]:
        probs = self._model.predict_proba(inputs)  # shape: (N, num_classes)

        elements = []
        for row in probs:
            best_idx = int(row.argmax())
            label = self._model.labels[best_idx]
            confidence = round(float(row[best_idx]), 3)
            elements.append(SpoilerElement(label=label, confidence=confidence))

        return elements
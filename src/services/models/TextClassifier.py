import transformers.training_args
from transformers.integrations.integration_utils import default_logdir as _default_logdir

if not hasattr(transformers.training_args, "default_logdir"):
    transformers.training_args.default_logdir = _default_logdir

from dataclasses import dataclass

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

    def predict(self, text: str):
        return self._model.predict(text)

    def batch_predict(self, texts: list[str]):
        pass
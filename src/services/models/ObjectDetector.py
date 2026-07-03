from dataclasses import dataclass, field
from .constants import *
from PIL import Image

from src.services.models.BaseModel import BaseModel


@dataclass
class GroundingDINO(BaseModel):
    model_id: str = field(default=OBJECT_DETECTOR_PATH)

    def __post_init__(self):
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForZeroShotObjectDetection.from_pretrained(self.model_id).to(DEVICE)
        self._model.eval()

    def predict(self, image: Image.Image, threshold: float = 0.3):
        import torch
        image = image.convert("RGB")

        inputs = self._processor(
            images=image,
            text=PROMPT,
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            outputs = self._model(**inputs)

        results = self._processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=threshold,
            text_threshold=threshold,
            target_sizes=[image.size[::-1]]
        )[0]

        return self.format_output(results)

    def batch_predict(self, image: Image.Image, threshold: float = 0.3):
        pass

    @staticmethod
    def format_output(results: dict) -> list:
        formatted = []
        for score, label, box in zip(results["scores"], results["text_labels"], results["boxes"]):
            formatted.append({
                "label": label,
                "confidence": round(score.item(), 3),
                "box": [round(i, 2) for i in box.tolist()]
            })
        return formatted
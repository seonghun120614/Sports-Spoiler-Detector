from dataclasses import dataclass, field
from .constants import *
from PIL import Image

from src.services.models.BaseModel import BaseModel
from src.domains.SpoilerInformation import SpoilerElement, BoundingBox, Point, ImageSpoiler
from src.services.models.utils import _clear

@dataclass
class GroundingDINO(BaseModel):
    model_id: str = field(default=OBJECT_DETECTOR_PATH)

    def __post_init__(self):
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForZeroShotObjectDetection.from_pretrained(self.model_id).to(DEVICE)
        self._model.eval()

    def predict(self, images: list[Image.Image], threshold: float = 0.3) -> list[list[ImageSpoiler]]:
        import torch

        inputs = self._processor(
            images=images,
            text=[PROMPT] * len(images),
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            outputs = self._model(**inputs)

        results = self._processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=threshold,
            text_threshold=threshold,
            target_sizes=[img.size[::-1] for img in images]
        )

        return self.format_output(results)


    @staticmethod
    def format_output(outputs: list[dict]) -> list[list[ImageSpoiler]]:
        outputs = _clear(outputs)
        result = []
        for objects in outputs:
            one = []
            for score, label, box in zip(objects["scores"], objects["text_labels"], objects["boxes"]):
                spoiler_elem = SpoilerElement(label=label, confidence=round(score, 2))
                left_top = Point(x=box[0], y=box[1])
                right_bottom = Point(x=box[2], y=box[3])
                bounding_box = BoundingBox(top_left=left_top, bottom_right=right_bottom)
                image_spoiler = ImageSpoiler.create(spoiler_elem=spoiler_elem, bounding_box=bounding_box)
                one.append(image_spoiler)
            result.append(one)
        return result
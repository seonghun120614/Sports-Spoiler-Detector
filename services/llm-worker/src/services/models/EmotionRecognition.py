from src.services.domains.SpoilerInformation import ImageSpoiler, SpoilerElement, BoundingBox, Point
from src.services.models.BaseModel import BaseModel

import numpy as np

class DeepFaceRecognition(BaseModel):

    def predict(self, bgr_images: list[np.ndarray]) -> list[list[ImageSpoiler]]:
        """Several Image Input"""

        if not bgr_images: return []
        from deepface import DeepFace
        result = []

        outputs = DeepFace.analyze(
            img_path=bgr_images,
            actions=["emotion"],
            enforce_detection=False,
        )

        for faces in outputs:
            one = []
            for face in faces:
                emotion = face['dominant_emotion']

                spoiler_elem = SpoilerElement(label = emotion,
                                              confidence = round(face['emotion'][emotion].item() / 100, 2))
                bounding_box = self._get_position(face['region'])

                img_spoiler = ImageSpoiler.create(spoiler_elem=spoiler_elem,
                                                  bounding_box=bounding_box)
                one.append(img_spoiler)
            result.append(one)
        return result

    def _get_position(self, region: dict[str, int]) -> BoundingBox:
        p1 = Point(x = region['x'], y = region['y'])
        p2 = p1.copy(x = region['x'] + region['w'],
                     y = region['y'] + region['h'])
        return BoundingBox(top_left = p1, bottom_right = p2)
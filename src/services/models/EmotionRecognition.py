from deepface import DeepFace

from src.services.models.BaseModel import BaseModel

import numpy as np

class DeepFaceRecognition(BaseModel):

    def extract(self, bgr_images: list[np.ndarray]) -> list[dict]:
        results = []

        for face_bgr in bgr_images:
            try:
                emotions = DeepFace.analyze(
                    img_path=face_bgr,
                    actions=["emotion"],
                    enforce_detection=False,
                )

                for emotion in emotions:
                    for e, prob in emotion['emotion'].items():
                        emotion['emotion'][e] = round(prob.item(), 2)

                return emotions
            except Exception as e:
                pass

        return results
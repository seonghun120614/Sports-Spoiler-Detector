from src.services.models.BaseModel import BaseModel

import numpy as np

class DeepFaceRecognition(BaseModel):

    def predict(self, bgr_images: list[np.ndarray]) -> list[dict]:
        from deepface import DeepFace
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

    def batch_predict(self, bgr_images: list[np.ndarray], threshold: float = 0.5):
        pass
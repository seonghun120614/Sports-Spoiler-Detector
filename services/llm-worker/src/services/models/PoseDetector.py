import math
import numpy as np

from PIL.Image import Image
from dataclasses import dataclass, field

from src.services.models.BaseModel import BaseModel
from .constants import *
from src.services.models.utils import _clear
from ..domains.SpoilerInformation import Point, BoundingBox, SpoilerElement, ImageSpoiler


@dataclass
class YoloV26Pose(BaseModel):
    model_id: str = field(default=POSE_DETECTOR_PATH)

    def __post_init__(self):
        from ultralytics import YOLO
        self._model = YOLO(self.model_id)
        self._model.to(DEVICE)

    def predict(self, images: list[Image], threshold: float = 0.5) -> list[list[ImageSpoiler]]:
        if not images: return []

        result = []
        outputs = self._model(images, conf=threshold)

        for r in outputs:
            one = []
            celebration = self.detect_celebration(r)

            for box, cel in zip(r.boxes, celebration):
                x1, y1, x2, y2 = _clear(box.xyxy[0].tolist())

                is_celebrating = cel['flags']['arms_wide_open'] or cel['flags']['knees_sliding']
                conf = round(box.conf[0].item(), 2) if is_celebrating else 0.0

                p1 = Point(x=x1, y=y1)
                p2 = Point(x=x2, y=y2)
                bounding_box = BoundingBox(top_left=p1, bottom_right=p2)

                spoiler_elem = SpoilerElement(label="celebration", confidence=conf)
                one.append(ImageSpoiler.create(spoiler_elem=spoiler_elem, bounding_box=bounding_box))
            result.append(one)

        return result

    @classmethod
    def calculate_angle(cls, p1: tuple, p2: tuple, p3: tuple) -> float:
        """
        세 점의 좌표를 기반으로 사잇각을 계산합니다.
        p2가 꼭짓점(Vertex)이 됩니다.
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # 역탄젠트(atan2)를 사용하여 두 선분이 x축과 이루는 각도를 각각 구한 뒤 차이를 계산
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        angle = abs(angle)

        # 내각을 구하기 위해 180도 이상일 경우 보정
        if angle > 180.0:
            angle = 360.0 - angle

        return angle

    @classmethod
    def detect_celebration(cls, player) -> list[dict]:
        """
        양팔 벌림(>= 90도)과 무릎 슬라이딩(<= 45도) 조건을 분석하여 논리값(Boolean)과 함께 반환합니다.
        """
        analysis_list = []

        if not player.keypoints or player.keypoints.xy is None:
            return analysis_list

        for kpts in player.keypoints.xy:
            kpts_np = kpts.cpu().numpy()

            # 1. 양팔-몸통 각도 (어깨가 꼭짓점: Hip - Shoulder - Elbow)
            l_arm_angle = cls.calculate_angle(
                kpts_np[KPT_MAP['L_HIP']], kpts_np[KPT_MAP['L_SHOULDER']], kpts_np[KPT_MAP['L_ELBOW']]
            ) if not np.all(kpts_np[KPT_MAP['L_SHOULDER']] == 0) else 0.0

            r_arm_angle = cls.calculate_angle(
                kpts_np[KPT_MAP['R_HIP']], kpts_np[KPT_MAP['R_SHOULDER']], kpts_np[KPT_MAP['R_ELBOW']]
            ) if not np.all(kpts_np[KPT_MAP['R_SHOULDER']] == 0) else 0.0

            # 2. 허벅지-종아리 각도 (무릎이 꼭짓점: Hip - Knee - Ankle)
            l_knee_angle = cls.calculate_angle(
                kpts_np[KPT_MAP['L_HIP']], kpts_np[KPT_MAP['L_KNEE']], kpts_np[KPT_MAP['L_ANKLE']]
            ) if not np.all(kpts_np[KPT_MAP['L_KNEE']] == 0) else 180.0  # 기본값 180 (직립)

            r_knee_angle = cls.calculate_angle(
                kpts_np[KPT_MAP['R_HIP']], kpts_np[KPT_MAP['R_KNEE']], kpts_np[KPT_MAP['R_ANKLE']]
            ) if not np.all(kpts_np[KPT_MAP['R_KNEE']] == 0) else 180.0

            # 3. 논리 조건 판별
            # 팔: 양쪽 중 하나라도 90도 이상이면 벌린 것으로 간주 (혹은 양쪽 모두(and)로 엄격하게 설정 가능)
            arms_wide_open = (l_arm_angle >= 90.0) or (r_arm_angle >= 90.0)

            # 무릎: 양쪽 무릎 중 하나라도 45도 이하로 굽혀졌는지 확인
            knees_sliding = (l_knee_angle <= 45.0) or (r_knee_angle <= 45.0)

            # 최종 세리머니 성립 여부
            is_celebration = arms_wide_open and knees_sliding

            analysis_list.append({
                "angles": {
                    "left_arm": round(l_arm_angle, 2),
                    "right_arm": round(r_arm_angle, 2),
                    "left_knee": round(l_knee_angle, 2),
                    "right_knee": round(r_knee_angle, 2)
                },
                "flags": {
                    "arms_wide_open": arms_wide_open,
                    "knees_sliding": knees_sliding,
                    "is_celebration_matched": is_celebration
                }
            })

        return analysis_list

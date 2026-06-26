import torch
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
NER_MODEL_PATH = BASE_DIR / "static" / "ner_model"
POSE_DETECTOR_PATH = BASE_DIR / "static" / "yolov8n-pose.pt"
OBJECT_DETECTOR_PATH = "IDEA-Research/grounding-dino-tiny"
SETFIT_MODEL_PATH = BASE_DIR / "static" / "soccer_spoiler_mpnet_v1"

if torch.cuda.is_available():
    device = "cuda"
elif torch.mps.is_available():
    device = "mps"
else:
    device = "cpu"

DEVICE = torch.device(device)

ENTITY_DESC = {
    "success": "A text that indicates a positive result of the match (victory, win, advance, etc.)",
    "failure": "A text that indicates a negative outcome of a match (defeat, elimination, relegation, etc.)",
    "draw": "A text indicating a state where the winner cannot be determined (draw, tie, etc.)",
    "round": "A text indicating the stage of a competition (finals, round of n, etc.) that implies the importance and timing of the match.",
    "name": "The name of a specific player or manager who is the protagonist of major events such as scoring, injury, or red card.",
    "scoring_text": "Text related to score changes, including expressions specifying scoring situations (multi-goal, hat-trick, etc.) and goals prevented (save, defensive success).",
    "special_event": "Special situations that drastically change the flow of the game or serve as key clues for predicting the outcome (red cards, penalties, own goals, injuries, hitting the post, etc.)",
    "emotive": "Modifiers and interjections imbued with subjective emotion regarding game results or situations (shocking, miraculous, insane, legendary, etc.)",
    "aftermath": "Structural repercussions or consequential events that occurred after the match ended (dismissal, resignation, retirement, worst signing, etc.)",
}

# COCO Keypoint Index 기준
KPT_MAP = {
    'NOSE': 0,
    'L_SHOULDER': 5, 'R_SHOULDER': 6,
    'L_ELBOW': 7,    'R_ELBOW': 8,
    'L_HIP': 11,     'R_HIP': 12,
    'L_KNEE': 13,    'R_KNEE': 14,
    'L_ANKLE': 15,   'R_ANKLE': 16
}

PROMPT = "player lifting a trophy. human face. face. ball. goal net."

NER_THRESHOLD = 0.5
from enum import Enum


class Action(Enum):
    ROTATE = "ROTATE"
    FLIP = "FLIP"


class DefectType(Enum):
    CRACK = "CRACK"
    POTHOLE = "POTHOLE"
    RAW = "RAW"


class Tone(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class FlipType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    BOTH = 2

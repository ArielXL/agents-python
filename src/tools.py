from enum import Enum

N = 0
E = 1
S = 2
W = 3
STAY = 4

class Constants(Enum):
    DIRTINESS_UP_60_PERCENT = 0
    CHILDREN_UNDER_CONTROL_CLEAN_HOUSE = 1
    TIME_OVER = 2

class States(Enum):
    N = 0
    E = 1
    S = 2
    W = 3
    STAY = 4

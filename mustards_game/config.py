"""Define constants and settings for the game"""
from copy import deepcopy

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
INFO_WIDTH = 500
MAX_ALTITUDE = 1000

OBSTACLES = [
    {"path": "sprites/mountain.png", "min": 600, "max": 900, "count": 3},
    {"path": "sprites/win_mountain.png", "min": 600, "max": 900, "count": 2},
    {"path": "sprites/blacksmith.png", "min": 10, "max": 200, "count": 2},
    {"path": "sprites/windmill.png", "min": 10, "max": 200, "count": 2},
]

NOT_OBSTACLES = [
    {"path": "sprites/Man.png", "min": 2, "max": 2, "count": 8},
    {"path": "sprites/Woman.png", "min": 2, "max": 2, "count": 8},
    {"path": "sprites/Old_man.png", "min": 2, "max": 2, "count": 8},
    {"path": "sprites/Old_Woman.png", "min": 2, "max": 2, "count": 8},
]

left_right = r"sprites/LeftRight.png"
up_down = r"sprites/UpDown.png"
padding_edge = r"sprites/padding_edge.png"
n_humans = sum([obj["count"] for obj in NOT_OBSTACLES])
n_obstacles = sum([obj["count"] for obj in OBSTACLES])

# make a copy of the lists to reset later
_OBST_REF = deepcopy(OBSTACLES)
_NOT_OBST_REF = deepcopy(NOT_OBSTACLES)

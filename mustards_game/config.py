"""Define constants and settings for the game"""
from copy import deepcopy
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
INFO_WIDTH = 500
MAX_ALTITUDE = 1000

OBSTACLES = [
    {"path": str(MODULE_DIR / "sprites" / "mountain.png"), "min": 600, "max": 900, "count": 3},
    {"path": str(MODULE_DIR / "sprites" / "win_mountain.png"), "min": 600, "max": 900, "count": 2},
    {"path": str(MODULE_DIR / "sprites" / "blacksmith.png"), "min": 10, "max": 200, "count": 2},
    {"path": str(MODULE_DIR / "sprites" / "windmill.png"), "min": 10, "max": 200, "count": 2},
]

NOT_OBSTACLES = [
    {"path": str(MODULE_DIR / "sprites" / "Man.png"), "min": 2, "max": 2, "count": 8},
    {"path": str(MODULE_DIR / "sprites" / "Woman.png"), "min": 2, "max": 2, "count": 8},
    {"path": str(MODULE_DIR / "sprites" / "Old_man.png"), "min": 2, "max": 2, "count": 8},
    {"path": str(MODULE_DIR / "sprites" / "Old_Woman.png"), "min": 2, "max": 2, "count": 8},
]

left_right = str(MODULE_DIR / "sprites" / "LeftRight.png")
up_down = str(MODULE_DIR / "sprites" / "UpDown.png")
padding_edge = str(MODULE_DIR / "sprites" / "padding_edge.png")
background_sprite = str(MODULE_DIR / "sprites" / "background.png")
ufo_sprite = str(MODULE_DIR / "sprites" / "ufo_25.png")
n_humans = sum([obj["count"] for obj in NOT_OBSTACLES])
n_obstacles = sum([obj["count"] for obj in OBSTACLES])

# make a copy of the lists to reset later
_OBST_REF = deepcopy(OBSTACLES)
_NOT_OBST_REF = deepcopy(NOT_OBSTACLES)

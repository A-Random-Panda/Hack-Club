'''Constants relating to the map maker'''

import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ursina import Entity

GRID_SIZE = (100, 100)
EDITOR_CAMERA_SPEED = 25

class CameraMode(enum.IntEnum):
    '''Describes whether the camera is in EditorCamera or FirstPersonController'''
    EDITOR = enum.auto()
    FIRST_PERSON = enum.auto()

class CameraControls():
    '''Variables relating to the camera'''
    camera_mode:CameraMode = CameraMode.EDITOR
    camera_dict:dict[CameraMode, "Entity"] = {}

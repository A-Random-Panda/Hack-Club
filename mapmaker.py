'''This hopefully will become a mapmaker for Ursina
Currently very WIP while I learn the library
'''

import json
import logging
import enum
from ursina import *

from scripts.player import _player_properties
from scripts.controls import Controls, get_binding
from scripts.editable_controls_FPC import FirstPersonController
from scripts.better_editor_camera import EditorCamera
from scripts.mapmaker_constants import *

#Declare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Create app
app = Ursina()

#Create grid
grid = Entity(model=Grid(*GRID_SIZE), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")

#test for now
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="PlayerModel", color=color.white, texture="Bamboo",rotation_x=0, y=0, enabled = True)

class CameraMode(enum.IntEnum):
    '''Describes whether the camera is in EditorCamera or FirstPersonController'''
    EDITOR = enum.auto()
    FIRST_PERSON = enum.auto()

class CameraControls():
    '''Variables relating to the camera'''
    camera_mode = CameraMode.EDITOR

fpc = FirstPersonController(**_player_properties)
fpc.disable()
editor_camera = EditorCamera()
editor_camera.enable()

def input(key):
    '''Input handler'''
    logger.debug("key %s pressed", key)
    ##Switch camera modes
    if key == get_binding(Controls.FREECAM_MODE):
        #Need to disable the other camera mode first before the enabling the second mode
        logger.info("Switch controls happening")
        fpc.disable()
        editor_camera.disable()

        if CameraControls.camera_mode == CameraMode.EDITOR:
            fpc.position = editor_camera.position
            fpc.rotation = (0, 0, 0)
            fpc.enable()
            CameraControls.camera_mode = CameraMode.FIRST_PERSON
        elif CameraControls.camera_mode == CameraMode.FIRST_PERSON:
            editor_camera.position = fpc.position
            editor_camera.rotation = (0, 0, 0)
            editor_camera.enable()
            CameraControls.camera_mode = CameraMode.EDITOR
        
        logger.debug("Editor camera state: %s", editor_camera.enabled)
        logger.debug("fpc state: %s", fpc.enabled)

def update():
    "Frame handler"
    if fpc.y < -2:
        fpc.position = (0, 2, 0)
    if CameraControls.camera_mode == CameraMode.FIRST_PERSON:
        player_shadow.disable()
    elif CameraControls.camera_mode == CameraMode.EDITOR:
        player_shadow.enable()
        player_shadow.position = editor_camera.position

app.run()
'''This hopefully will become a mapmaker for Ursina
Currently very WIP while I learn the library
'''

import json
import logging
from ursina import *
from scripts.player import _player_properties
from scripts.controls import Controls, get_binding
from scripts.editable_controls_FPC import FirstPersonController
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

fpc = FirstPersonController(**_player_properties)
fpc.disable()

editor_camera = EditorCamera()
editor_camera.enable()


def input(key):
    logger.debug("key %s pressed", key)
    ##Switch camera modes
    if key == get_binding(Controls.FREECAM_MODE):
        logger.info("Switch controls happenning")
        editor_camera.enabled = not editor_camera.enabled
        fpc.enabled = not fpc.enabled
        logger.info("Editor camera state: %s", editor_camera.enabled)
        logger.info("fpc state: %s", fpc.enabled)

app.run()
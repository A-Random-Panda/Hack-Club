'''This hopefully will become a mapmaker for Ursina
Currently very WIP while I learn the library
'''

import logging
from typing import override
import math
import enum

from ursina import *
from scripts.player import _player_properties
from scripts.controls import Controls, get_binding
from scripts.editable_controls_FPC import FirstPersonController as edited_fpc
from scripts.better_editor_camera import EditorCamera
from scripts.mapmaker.mapmaker_constants import *
from scripts.mapmaker.map_save import save_map

#Declare logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Create app
app = Ursina()

class CameraMode(enum.IntEnum):
    '''Describes whether the camera is in EditorCamera or FirstPersonController'''
    EDITOR = enum.auto()
    FIRST_PERSON = enum.auto()

class CameraControls():
    '''Variables relating to the camera'''
    camera_mode:CameraMode = CameraMode.EDITOR
    camera_dict:dict[CameraMode, Entity] = {}


#Harry sucks so I have to do this
class FirstPersonController(edited_fpc):
    '''
    Basically the update and physics update aren't in the same function
    so I need to do this
    '''
    @override
    def update(self):
        super().update()
        super().physics_update()

def normal_round(value:int|float) -> int:
    '''
    Python does banker's rounding... which really messes up this code
    This function just implements normal rounding in one line
    '''
    return math.copysign(math.floor(abs(value) + 0.5), value) #type: ignore

#Creatinng textures
grid = Entity(model=Grid(*GRID_SIZE), scale=Vec3(100, 100), color=color.white, rotation_x=90, position=Vec3(.5, .5, .5), collider ="box")
entitylist = []
player_shadow = Entity(model="PlayerModel", color=color.white, texture="Bamboo",rotation_x=0, y=0)
player_line = Entity(model = Quad(radius=200, mode='line'), color=color.white)
last_hit_line = Entity(model=Mesh(mode="line",vertices=((0,0,0),(0,100,0)), thickness=3),
                       enabled=False,)
line1 = Entity(model=Mesh(mode="line",vertices=((50,0,50),(50,100,50)), thickness=3))
line2 = Entity(model=Mesh(mode="line",vertices=((-50,0,50),(-50,100,50)), thickness=3))
line3 = Entity(model=Mesh(mode="line",vertices=((50,0,-50),(50,100,-50)), thickness=3))
line4 = Entity(model=Mesh(mode="line",vertices=((-50,0,-50),(-50,100,-50)), thickness=3))

player_line.add_to_scene_entities = False
player_shadow.add_to_scene_entities = False

fpc = FirstPersonController(**_player_properties)
fpc.disable()
editor_camera = EditorCamera(move_speed=EDITOR_CAMERA_SPEED)
editor_camera.enable()

CameraControls.camera_dict.update({CameraMode.EDITOR: editor_camera, CameraMode.FIRST_PERSON: fpc})

def input(key):
    '''Input handler'''
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

    if key == get_binding(Controls.PLACE_CAMERA):
        #Place block
        if mouse.hovered_entity:
            last_hit_line.enable()
            logger.debug("Mouse at point %s.", mouse.world_point)
            last_hit_line.position = mouse.world_point
            pos = mouse.world_point
            assert pos is not None
            #Sets the position to the nearest whole block
            pos.x_setter(normal_round(pos.x_getter()))
            pos.y_setter(normal_round(pos.y_getter()))
            pos.z_setter(normal_round(pos.z_getter()))
            #Placing the entity into the world
            logger.debug("Placing entity at %s.", pos)
            entitylist.append(Entity(model="cube",
                                    scale=Vec3(1,1,1),
                                    color=color.red,
                                    collider = "box",
                                    position = pos))

    if key == get_binding(Controls.RESET_CAMERAS):
        #Reset map
        logger.info("Entity list reset")
        for entity in entitylist:
            destroy(entity)
        entitylist.clear()

    if key == "\\":
        #Save
        save_map(entitylist)

def update():
    "Frame handler"
    if fpc.y < -10:
        fpc.position = (0, 2, 0)
    if CameraControls.camera_mode == CameraMode.FIRST_PERSON:
        player_line.disable()
        player_shadow.disable()
    elif CameraControls.camera_mode == CameraMode.EDITOR:
        player_shadow.enable()
        player_line.enable()
        player_line.position = editor_camera.position
        player_line.rotation = editor_camera.rotation
        player_shadow.world_position = editor_camera.world_position

app.run()
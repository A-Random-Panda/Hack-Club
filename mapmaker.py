'''
This is an internal tool that is / will be used to make maps
Currently, for time reasons, this is unfinished, and the only map in the game is hand coded
But hopefully, if more maps are to be made in the future, they should be made using this tool
'''

import logging
from typing import override
import math
import enum

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from scripts.game.player import _player_properties
from scripts.game.controls import Controls, get_binding
from scripts.helper.better_editor_camera import EditorCamera
from scripts.mapmaker.mapmaker_constants import *
from scripts.mapmaker.mapmaker_helper import *
from scripts.mapmaker.map_save import save_map

#Declare logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Create app
app = Ursina()

#Creatinng textures
grid = Entity(model=Grid(*GRID_SIZE), scale=Vec3(100, 100), color=color.white, rotation_x=90, position=Vec3(.5, .5, .5), collider ="box")
entitylist = []
player_shadow = Entity(model="Better_Tank", color=color.red, rotation_x=0, y=0,scale = 0.5, collider="mesh")
player_line = Entity(model = Quad(radius=200, mode='line'), color=color.white)
last_hit_line = Entity(model=Mesh(mode="line",vertices=((0,0,0),(0,100,0)), thickness=3),
                       enabled=False,)
line1 = Entity(model=Mesh(mode="line",vertices=((50,0,50),(50,100,50)), thickness=3))
line2 = Entity(model=Mesh(mode="line",vertices=((-50,0,50),(-50,100,50)), thickness=3))
line3 = Entity(model=Mesh(mode="line",vertices=((50,0,-50),(50,100,-50)), thickness=3))
line4 = Entity(model=Mesh(mode="line",vertices=((-50,0,-50),(-50,100,-50)), thickness=3))
wall1 = Entity(model="cube", scale=(50,12,0.3), color=color.red, collider = "box", x=0, z=-25)

player_line.add_to_scene_entities = False
player_shadow.add_to_scene_entities = False

fpc = FirstPersonController(**_player_properties)
fpc.collider = None
fpc.disable()
editor_camera = EditorCamera(move_speed=EDITOR_CAMERA_SPEED)
editor_camera.enable()

CameraControls.camera_dict.update({CameraMode.EDITOR: editor_camera, CameraMode.FIRST_PERSON: fpc})


def game_input_handler(key):
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
            normal = mouse.normal
            assert pos is not None
            assert normal is not None
            pos.x_setter(game_round(pos.x_getter(), normal.x_getter()))
            pos.z_setter(game_round(pos.z_getter(), normal.z_getter()))
            pos.y_setter(game_round(pos.y_getter(), normal.y_getter()))
            #Placing the entity into the world
            logger.debug("Placing entity at %s. Mouse normal %s, Mouse pos %s", pos, mouse.normal, mouse.world_point)
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

input = game_input_handler

app.run() #type: ignore

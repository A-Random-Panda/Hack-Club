"""
This is the main file that will run the game
"""

from ursina import *
from scripts.controls import *
from scripts.editable_controls_FPC import FirstPersonController as FPC
import logging
import asyncio
import websockets
import threading
import json
import queue
import socket

#Declare logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

mode = input("Host or join (h/j) ").strip().lower()
if mode == "j":
    ip = input("input host ip ").strip()
else:
    print("your ip is ", socket.gethostbyname(socket.gethostname()))

#Create app
app = Ursina()

#Importing models
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="PlayerModel", color=color.white,texture="Bamboo",rotation_x=0, y=0, enabled = False)

#Setup
camoverlay = Text (parent= camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
camoverlay.disable()

player = FPC(
    texture = "Bamboo.png",
    model="PlayerModel.obj",
    collider="box",
    position = (0.5,1,0.5),
    speed = 20,
    jump_height=4,
    gravity = 1
)
player.visible = False

# Walls
wall1 = Entity(model="cube", scale=(50,12,1), color=color.red, collider = "box", x=0, z=-24)
wall2 = Entity(model="cube", scale=(50,12,1), color=color.green, collider = "box", x=0, z=24)
wall3 = Entity(model="cube", scale=(50,12,1), color=color.blue, collider = "box", x=-24, z=0, rotation_y=90)
wall4 = Entity(model="cube", scale=(50,12,1), color=color.black, collider = "box", x=24, z=0, rotation_y=90)

wall1 = Entity(model="cube", scale=(50,12,1), color=color.red, collider = "box", x=0, z=-25)
wall2 = Entity(model="cube", scale=(50,12,1), color=color.green, collider = "box", x=0, z=25)
wall3 = Entity(model="cube", scale=(50,12,1), color=color.blue, collider = "box", x=-25, z=0, rotation_y=90)
wall4 = Entity(model="cube", scale=(50,12,1), color=color.black, collider = "box", x=25, z=0, rotation_y=90)

start=Entity(model="cube", scale=(2,1,2), color=color.red, collider="box", x=0, z=0)
end=Entity(model="cube", scale=(2,1,2), color=color.green, collider="box", x=0, z=20)

#Other objects
cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')
cube.rotation_y = 90
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')
print(scene.entities, "")

#Variable declarations
camera_entity_list = [player]
saved_pos = (0.5,1,0.5)
saved_rot = (0,0,0)
in_camera = False
current_cam = 0

def input(key):
    '''Input handler'''
    global saved_pos
    global saved_rot
    global in_camera
    global current_cam
    global camera_entity_list

    if key == get_binding(Controls.TOGGLE_CAMERA): # camera
        current_cam += 1
        if current_cam == len(camera_entity_list):
            current_cam = 0

        if current_cam == 0 and len(camera_entity_list) != 1: #player
            player.texture = "Bamboo.png"
            player.model="PlayerModel.obj"
            player.position = saved_pos
            player.speed = 20
            player.jump_height=4
            player.gravity = 1
            in_camera = False
            camoverlay.disable()
        elif current_cam != 0:
            saved_pos = player_shadow.position
            saved_rot = player_shadow.rotation
            player.texture ="cam"
            player.model = "cypher_cam"
            player.position = camera_entity_list[current_cam].position
            player.rotation = (0,camera_entity_list[current_cam].rotation[1]+180,0)

            player.speed = 0
            player.jump_height=0
            player.gravity = 0
            in_camera = True
            camoverlay.enable()
            camoverlay.text= f'cam {current_cam}'     

    if key == get_binding(Controls.RESET_CAMERAS): # reset
        current_cam = 0
        for i in range(1,len(camera_entity_list)):
            destroy(camera_entity_list[i])
        player.position = saved_pos
        player.rotation = saved_rot
        player.speed = 20
        player.jump_height=4
        player.gravity = 1
        in_camera = False
        camoverlay.disable()
        camera_entity_list.clear()
        camera_entity_list = [player]

    if key == get_binding(Controls.PLACE_CAMERA):
        hit = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player] + camera_entity_list)
        if hit.hit and not in_camera:
            dist = any(distance(hit.world_point, n.position) < 1 for n in camera_entity_list)
            if not dist:
                camera_entity_list.append(Entity(model = 'cypher_cam',
                                color = color.orange,
                                collider = 'box',
                                position = hit.world_point,
                                texture = "cam",
                                rotation = (180,player.rotation[1],180)))

    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)

    if key == get_binding(Controls.QUIT_GAME):
        application.quit()

def update():
    "Frame handler"
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)

    if not in_camera: #Actually player movement
        player_shadow.enabled = True
        player_shadow.position = player.position
        player_shadow.rotation = player.rotation

app.run()
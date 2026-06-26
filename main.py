"""
This is the main file that will run the game
"""
import logging
import socket
from ursina import *
from scripts.controls import *
from scripts.player import get_player

#Declare logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#Create app
app = Ursina()

#Importing models
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="PlayerModel", color=color.white,texture="Bamboo",rotation_x=0, y=0, enabled = False)

#Setup
camoverlay = Text (parent= camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
camoverlay.disable()

player = get_player()
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

#Variable declarations
player.perspective_list = [player]

def input(key):
    '''Input handler'''
    #Enter cameras
    if key == get_binding(Controls.TOGGLE_CAMERA):
        player.current_cam += 1
        #Camera rollover
        if player.current_cam == len(player.perspective_list):
            player.current_cam = 0
        #If the camera is on the player and there is at least one camera
        if player.current_cam == 0 and len(player.perspective_list) > 1: #player
            player.in_camera = False
            camoverlay.disable()
            player.perspective_list[-1].visible = True
            camera.parent = player.camera_pivot
        elif player.current_cam != 0:
            camera.parent = player.perspective_list[player.current_cam].camera_pivot
            player.perspective_list[player.current_cam].visible = False
            player.perspective_list[player.current_cam-1].visible = True
            player.in_camera = True
            camoverlay.enable()
            camoverlay.text= f'cam {player.current_cam}'
    #Reset cameras
    if key == get_binding(Controls.RESET_CAMERAS):
        player.current_cam = 0
        for i in range(1,len(player.perspective_list)):
            destroy(player.perspective_list[i])
        player.speed = 20
        player.jump_height=4
        player.gravity = 1
        player.in_camera = False
        camera.parent = player.camera_pivot
        camoverlay.disable()
        player.perspective_list.clear()
        player.perspective_list.append(player)
    #Placing camera
    if key == get_binding(Controls.PLACE_CAMERA):
        hit = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player] + player.perspective_list)
        if hit.hit and not player.in_camera:
            dist = any(distance(hit.world_point, n.position) < 1 for n in player.perspective_list)
            if not dist:
                temp_cam = (Entity(model = 'cypher_cam',
                                collider = 'box',
                                position = hit.world_point,
                                texture = "cam",
                                rotation = (180,player.rotation[1],180)))
                temp_cam.camera_pivot = Entity(parent=temp_cam, y = 1.6)
                player.perspective_list.append(temp_cam)

    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)
    #Exit game
    if key == get_binding(Controls.QUIT_GAME):
        application.quit()

def update():
    "Frame handler"
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)

    if not player.in_camera: #Actually player movement
        player_shadow.enabled = True
        player_shadow.position = player.position
        player_shadow.rotation = player.rotation
print("this is a change")
app.run()
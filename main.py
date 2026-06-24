from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as FPC
import asyncio
import websockets
import threading
import json
import queue
import socket

mode = input("Host or join (h/j) ").strip().lower()
if mode == "j":
    ip = input("input host ip ").strip()
else:
    print("your ip is ", socket.gethostbyname(socket.gethostname()))



app = Ursina()
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
playerShadow = Entity(model="PlayerModel", color=color.white,texture="Bamboo",rotation_x=0, y=0, enabled = False)
camlist= [playerShadow.position]

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
camoverlay = Text (parent= camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
camoverlay.disable()

saved_pos = (0.5,1,0.5)
cam = False
cams = []
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
count = 0
def input(key): 
    global saved_pos
    global cam
    global camlist
    """
    if key == "f": # player
        player.texture = "Bamboo.png"
        player.model="PlayerModel.obj"
        player.position = saved_pos
        player.speed = 20
        player.jump_height=4
        player.gravity = 1
        cam = False
    """
    if key == "c": # cam
        global count
        count += 1
        if count == len(camlist):
            count = 0
        '''
        saved_pos = playerShadow.position
        player.texture ="cam"
        player.model = "cypher_cam"
        player.position = (5,5,5)
        player.speed = 0
        player.jump_height=0
        player.gravity = 0
        cam = True
        '''

        if count == 0 and len(camlist) != 1: #player
            player.texture = "Bamboo.png"
            player.model="PlayerModel.obj"
            player.position = saved_pos
            player.speed = 20
            player.jump_height=4
            player.gravity = 1
            cam = False
            camoverlay.disable()
        elif count != 0:
            saved_pos = playerShadow.position
            player.texture ="cam"
            player.model = "cypher_cam"
            player.position = camlist[count]
            player.speed = 0
            player.jump_height=0
            player.gravity = 0
            cam = True
            camoverlay.enable()
            camoverlay.text= f'cam {count}'
        

    if key == "r": # reset
        camlist = [playerShadow.position]
        count = 0
        for i in cams:
            destroy(i)
        player.position = saved_pos
        player.speed = 20
        player.jump_height=4
        player.gravity = 1
        cam = False
        camoverlay.disable()

    if key == 'left mouse down': #placing cameras
        hit = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player] + cams)
        if hit.hit and cam == False:
           cams.append(Entity(model = 'cypher_cam', color = color.orange, collider = 'box', position = hit.world_point,texture="cam", rotation = (player.rotation[0]+180,player.rotation[1],player.rotation[2]+180)))
           camlist.append(hit.world_point)
           pass

    if key == 'p': #freecam mode
        EditorCamera(enabled=True)

    if key == "escape":
        application.quit()

def update():
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)
    
    
    if cam == False: #Actually player movement
        playerShadow.enabled = True
        playerShadow.position = player.position
        
        




cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')

cube.rotation_y = 90
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')
print(scene.entities, "")
app.run()
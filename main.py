from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as FPC

app = Ursina()
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")

# Walls
wall1 = Entity(model="cube", scale=(50,12,1), color=color.red, collider = "box", x=0, z=-24)
wall2 = Entity(model="cube", scale=(50,12,1), color=color.green, collider = "box", x=0, z=24)
wall3 = Entity(model="cube", scale=(50,12,1), color=color.blue, collider = "box", x=-24, z=0, rotation_y=90)
wall4 = Entity(model="cube", scale=(50,12,1), color=color.black, collider = "box", x=24, z=0, rotation_y=90)

start=Entity(model="cube", scale=(2,1,2), color=color.red, collider="box", x=0, z=0)
end=Entity(model="cube", scale=(2,1,2), color=color.green, collider="box", x=0, z=20)

#obstactles
saved_pos = (0.5,1,0.5)
cam = True

player = FPC(
    texture = "Bamboo.png",
    model="PlayerModel.obj",
    collider="box",
    position = (0.5,1,0.5),
    speed = 20,
    jump_height=4,
    gravity = 1
)
player.visible = True


def input(key): #player
    global saved_pos
    if key == "f":
        player.texture = "Bamboo.png"
        player.model="PlayerModel.obj"
        player.position = saved_pos
        player.speed = 20
        player.jump_height=4
        player.gravity = 1
        player.visible = True
    if key == "escape":
        application.quit()

    if key == "c": #cam
        saved_pos = player.position
        player.texture ="cam"
        player.model = "cypher_cam"
        player.position = (5,5,5)
        player.speed = 0
        player.jump_height=0
        player.gravity = 0
        
        player.visible = True
    
    if key == 'p':
        EditorCamera(enabled=True)
        player.visible = True
    if key == 'l':
        EditorCamera(enabled=False)
        player.visible = True
    

def update():
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)


cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')

cube.rotation_y = 90
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')
app.run()
from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as FPC

app = Ursina()
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")

# Walls
wall1 = Entity(model="cube", scale=(20,12,1), color=color.rgb(100,110,120), collider = "box", x=0, z=-2)
wall2 = Entity(model="cube", scale=(20,12,1), color=color.rgb(100,110,120), collider = "box", x=0, z=22)
wall3 = Entity(model="cube", scale=(20,12,1), color=color.rgb(100,110,120), collider = "box", x=-10, z=1, rotation_y=90)
wall4 = Entity(model="cube", scale=(20,12,1), color=color.rgb(100,110,120), collider = "box", x=10, z=10, rotation_y=90)

start=Entity(model="cube", scale=(2,1,2), color=color.red, collider="box", x=0, z=0)
end=Entity(model="cube", scale=(2,1,2), color=color.green, collider="box", x=0, z=20)

#obstactles
pos = ()
cam = True

player = FPC(
    model=None,
    collider="box",
    position = (0.5,1,0.5),
    speed = 20,
    jump_height=4,
    gravity = 1
)
player.visible = False


def input(key): #player
    global pos
    global player
    if key == "f":
        pos = player.position
        player = FPC(
            position = pos,
            speed = 20,
            jump_height=4,
            gravity = 1
        )
    if key == "escape":
        application.quit()

    if key == "c": #cam
        pos = player.position
        player = FPC(
            position = (5,5,5),
            speed = 0,
            jump_height=0,
            gravity = 0
        )
def update():
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)


cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')

cube.rotation_y = 90
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')
cube1.x += 10
app.run()
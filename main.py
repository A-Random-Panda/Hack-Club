"""
This is the main file that will run the game
"""
import logging
import socket
from ursina import *
from scripts.controls import *
from scripts.player import get_player
import time

#Declare logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#Settings
player_sensitivity = 150
player_volume = 1.5


#Create app
app = Ursina()

#Importing models
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="PlayerModel", color=color.white,texture="Bamboo",rotation_x=0, y=0, enabled = False)

#Initializing sounds
shooting = Audio("sniper_shot",autoplay=False, volume= 0.5)
success = Audio("success",autoplay = False, volume = player_volume)
death = Audio("death",autoplay = False, volume = player_volume)

#Setup
camoverlay = Text (parent= camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
camoverlay.disable()
player = get_player()
player.visible = False
player.cd = time.perf_counter()
player.collider = MeshCollider(player, mesh = player.model)

#Enters / Exists UIs
def ui_changer(boolean = False):
    for button in button_list:
        button.enabled = button.enabled = boolean
def open_volume_menu(boolean = True):
    ui_changer()
    volume_slider.enabled = boolean

#Used to change volume
def change_volume():
    shooting.volume = (volume_slider.value/100)

#Sliders
volume_slider = ThinSlider(text='Gun Volume', dynamic=True, max = 100, step = 1, enabled = False, default = 50, on_value_changed = change_volume)
volume_slider.label.origin = (0,0)
volume_slider.label.position = (.25, -.1)


#Buttons
button_list = []
quit_button = Button(model = "quad", scale = 0.2, x = 0, color=color.gray, text = "Quit Game", text_size = 0.8, text_color = color.black, enabled = False)
quit_button.on_click = application.quit
volume_button = Button(model = "quad", scale = 0.2, x = 0.2, color = color.gray, text = "volume controls", text_size = 0.8, text_color = color.black, enabled = False)
volume_button.on_click = open_volume_menu

control_button = Button(model = "quad", scale = 0.2, x = -0.2, color = color.gray, text = "controls", text_size = 0.8, text_color = color.black, enabled = False)
button_list.extend([volume_button,quit_button,control_button])

#Walls

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
        player.rotation[1] = 90
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
    #Shooting
    if key == get_binding(Controls.SHOOT):
        if 5 < abs(time.perf_counter()-player.cd):
            hit = raycast(origin = player.world_position + player.forward,distance=1000, direction = player.forward)
            player.cd = time.perf_counter()
            shooting.play()
            player.bullet_trail = Entity(model="cube",
                                         position= ((hit.world_point + player.world_position+player.forward)/2) + Vec3(0,1.7,0),
                                         scale = (0.2,0.2,distance(hit.world_point,player.world_position)),
                                         color = color.white,parent = scene,
                                         rotation = player.rotation,
                                         collider = "box"
                                         )
            destroy(player.bullet_trail,delay = 0.1)




    #Reset cameras
    if key == get_binding(Controls.RESET_CAMERAS):
        player.current_cam = 0
        for i in range(1,len(player.perspective_list)):
            destroy(player.perspective_list[i])
        player.in_camera = False
        camera.parent = player.camera_pivot
        camoverlay.disable()
        player.perspective_list.clear()
        player.perspective_list.append(player)

    #Placing camera
    if key == get_binding(Controls.PLACE_CAMERA):
        infront = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player] + player.perspective_list)
        if infront.hit and not player.in_camera and not player.in_menu:
            dist = any(distance(infront.world_point, n.position) < 1 for n in player.perspective_list)
            if not dist:
                temp_cam = (Entity(model = 'cypher_cam',
                                position = infront.world_point,
                                texture = "cam",
                                rotation = (180,player.rotation[1],180)))
                temp_cam.camera_pivot = Entity(parent=temp_cam, y = 1.6)
                player.perspective_list.append(temp_cam)
                temp_cam.original_rotation_y = temp_cam.rotation_y
                temp_cam.collider = MeshCollider(temp_cam, mesh = temp_cam.model)

    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)

    #Escape menu
    if key == get_binding(Controls.QUIT_GAME):
        player.in_menu = not player.in_menu
        #Buttons
        if player.in_menu:
            mouse.visible = True
            mouse.locked = False
            player.cursor.enabled = False
            ui_changer(True)
        else:
            mouse.visible = False
            mouse.locked = True
            player.cursor.enabled = True
            open_volume_menu(False)




def update():
    "Frame handler"
    if held_keys[get_binding(Controls.CAMERA_LEFT)]:
        player_shadow.rotation_y -= player_sensitivity * time.dt
    
    if held_keys[get_binding(Controls.CAMERA_RIGHT)]:
        player_shadow.rotation_y += player_sensitivity * time.dt
    
    if player.y < -2:
        player.position = (0.5, 1.0,0.5)
    if not player.in_camera:
        player_shadow.enabled = False
        player_shadow.position = player.position
        player_shadow.rotation = (player.rotation[0]+180,player.rotation[1],player.rotation[2]+180)
    else:
        player_shadow.enabled = True
        player_shadow.position = player.position
        player.rotation_y = player_shadow.rotation_y

    if player.bullet_trail and player.bullet_trail.intersects(player).hit:
        death.play()

    #Escape menu


app.run()
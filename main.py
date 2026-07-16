"""
This is the main file that will run the game
"""
import logging
import time
import subprocess

from ursina import *

from scripts.controls import *
from scripts.player import get_player
from scripts.death import DeathManager
from scripts.minimap import UpdateMinimap, MinimapIcons
from scripts.combat import shoot, reload_timer
from scripts.audio_controller import AudioController
from scripts.settings import *
from scripts.ui import UIController

#Moving block for testing
moving_block = Entity(model="cube", color = color.yellow, position=(0,4,3),collider = "box", scale = (1,5,1))
speed123 = 5*time.dt
multi = 1
enable_moving_block = True
test = False
#Declare logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



#Create app
app = Ursina(icon="assets/textures/ursina.ico")

#Objects on the map
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="PlayerModel", color=color.white,texture="Bamboo",rotation_x=0, y=0, enabled = False)
#cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')

#Walls
wall1 = Entity(model="cube", scale=(50,12,1), color=color.red, collider = "box", x=0, z=-25)
wall2 = Entity(model="cube", scale=(50,12,1), color=color.green, collider = "box", x=0, z=25)
wall3 = Entity(model="cube", scale=(50,12,1), color=color.blue, collider = "box", x=-25, z=0, rotation_y=90)
wall4 = Entity(model="cube", scale=(50,12,1), color=color.black, collider = "box", x=25, z=0, rotation_y=90)


#Setup
player = get_player()
player.visible = False
player.cd = time.perf_counter()
player.collider = MeshCollider(player, mesh = player.model)
player.previous_x = player.x
player.previous_y = player.y
uicontroller = UIController(player,mouse)



#Shop upgrade functions
def cam_upgrade():
    current_upgrade = player.max_cams-5
    if current_upgrade == len(MAX_CAM_COST)-1 and player.cash >= MAX_CAM_COST[current_upgrade]:
        player.cash -= MAX_CAM_COST[current_upgrade]
        uicontroller.current_cash.text = f"{player.cash} cash"
        player.max_cams += 1
        uicontroller.upgrade_cams_button.text = f"current cams: {player.max_cams} \n MAXED OUT"
        audio_controller.success.play()
    elif current_upgrade < len(MAX_CAM_COST) and player.cash >= MAX_CAM_COST[current_upgrade]:
        player.cash -= MAX_CAM_COST[current_upgrade]
        uicontroller.current_cash.text = f"{player.cash} cash"
        next_cost = MAX_CAM_COST[current_upgrade + 1]
        player.max_cams += 1
        uicontroller.upgrade_cams_button.text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${next_cost}"
        audio_controller.success.play()

def reload_upgrade():
    current_upgrade = int((5-player.reload_time)/0.5)
    if current_upgrade == len(FASTER_RELOAD_COST)-1 and player.cash >= FASTER_RELOAD_COST[current_upgrade]:
        player.cash -= FASTER_RELOAD_COST[current_upgrade]
        uicontroller.current_cash.text = f"{player.cash} cash"
        player.reload_time -= 0.5
        uicontroller.faster_reload_button.text = f"reload time: {player.reload_time} \n MAXED OUT"
        audio_controller.success.play()
    elif current_upgrade < len(FASTER_RELOAD_COST) and player.cash >= FASTER_RELOAD_COST[current_upgrade]:
        player.cash -= FASTER_RELOAD_COST[current_upgrade]
        uicontroller.current_cash.text = f"{player.cash} cash"
        next_cost = FASTER_RELOAD_COST[current_upgrade + 1]
        player.reload_time -= 0.5
        uicontroller.faster_reload_button.text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${next_cost}"
        audio_controller.success.play()


#Buttons in shop menu
uicontroller.upgrade_cams_button.on_click = cam_upgrade
uicontroller.faster_reload_button.on_click = reload_upgrade

#Buttons in main menu
uicontroller.quit_button.on_click = application.quit
uicontroller.volume_button.on_click = uicontroller.open_volume_menu
uicontroller.control_button.on_click = uicontroller.open_control_menu


#Control change buttons
uicontroller.reset_controls_to_default_button.on_click = uicontroller.reset_and_update_controls


def cam_switching():
    if player.current_cam == len(player.perspective_list):
            player.current_cam = 0
        #If the camera is on the player and there is at least one camera
    if player.current_cam == 0 and len(player.perspective_list) > 1: #player
        player.in_camera = False
        uicontroller.camoverlay.disable()
        player.perspective_list[-1].visible = True
        camera.parent = player.camera_pivot
    elif player.current_cam != 0:
        camera.parent = player.perspective_list[player.current_cam].camera_pivot
        player.perspective_list[player.current_cam].visible = False
        player.perspective_list[player.current_cam-1].visible = True
        player.in_camera = True
        uicontroller.camoverlay.enable()
        uicontroller.camoverlay.text= f'cam {player.current_cam}'

#Variable declarations
player.perspective_list = [player]
minimap_icons = MinimapIcons()
audio_controller = AudioController(player)
death_manager = DeathManager(player, audio_controller, uicontroller, player_shadow,cam_switching)
update_player_icon = UpdateMinimap(minimap_icons.player_icon,player,55)
update_moving_square_icon = UpdateMinimap(minimap_icons.square_icon,moving_block,55)

#Functions to change the volume
def gun_change_volume():
    audio_controller.set_gun_volume(uicontroller.gun_volume_slider.value)

def player_change_volume():
    audio_controller.set_player_volume(uicontroller.player_volume_slider.value)

#Sound sliders
uicontroller.gun_volume_slider.on_value_changed = gun_change_volume
uicontroller.player_volume_slider.on_value_changed = player_change_volume

#Detect key inputs
def input(key):
    global test
    '''Input handler'''
     #Escape menu
    if key == get_binding(Controls.QUIT_GAME) and not player.in_shop:
        player.in_menu = not player.in_menu
        #Buttons
        if player.in_menu:
            mouse.visible = True
            mouse.locked = False
            player.cursor.enabled = False
            uicontroller.ui_changer(True)
            uicontroller.menu_overlay.enabled = True
        else:
            mouse.visible = False
            mouse.locked = True
            player.cursor.enabled = True
            uicontroller.open_volume_menu(False)
            uicontroller.open_control_menu(False)
    
    if key == get_binding(Controls.QUIT_GAME) and player.in_shop:
        player.in_shop = False
        uicontroller.open_shop_menu(False)

    
    if player.control_change_button_pressed:
        if isinstance(key, str) and "mouse" not in key and "escape" not in key:
            player.changed_key = key
            player.control_change_button_pressed = False
    

    if not player.input_enabled:
        return
    #Enter cameras
    if key == get_binding(Controls.TOGGLE_CAMERA):
        player.current_cam += 1
        player.rotation[1] = 90
        #Camera rollover
        cam_switching()
    #Shooting
    if key == get_binding(Controls.SHOOT):
        shoot(player,audio_controller.reload,audio_controller.shooting)


    #Reset cameras
    if key == get_binding(Controls.RESET_CAMERAS):
        player.current_cam = 0
        for i in range(1,len(player.perspective_list)):
            destroy(player.perspective_list[i])
        for icons in player.cam_icon_list:
            destroy(icons)
        player.in_camera = False
        camera.parent = player.camera_pivot
        uicontroller.camoverlay.disable()
        player.perspective_list.clear()
        player.perspective_list.append(player)

    #Placing camera
    if key == get_binding(Controls.PLACE_CAMERA) and not player.in_menu and not player.in_shop and not len(player.perspective_list) > player.max_cams:
        infront = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player] + player.perspective_list)
        if infront.hit and not player.in_camera:
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
                cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = temp_cam.x/55,y= temp_cam.z/55, model = "quad", texture = "camera_icon", scale = 0.05)
                player.cam_icon_list.append(cam_icon)
        
    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)

   
    #Jumping sound
    if key == get_binding(Controls.JUMP) and player.grounded:
        audio_controller.jump.play()
    
    #Open shop menu
    if key == get_binding(Controls.OPEN_SHOP) and not player.in_menu:
        player.in_shop = not player.in_shop
        if player.in_shop:
            uicontroller.open_shop_menu(True)
        else:
            uicontroller.open_shop_menu(False)

    if key ==  "t":
        test = True


def update():
    global test
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

    #Footstep sounds
    if player.x != player.previous_x and not audio_controller.footsteps.playing and not player.y != player.previous_y:
        audio_controller.footsteps.play()
    if (player.x == player.previous_x or not player.grounded) and audio_controller.footsteps.playing:
        audio_controller.footsteps.stop()
    player.previous_x = player.x
    player.previous_y = player.y
    
    #Changes controls
    if player.changed_key is not None:
        set_control(player.control_change_key, player.changed_key)
        player.changed_key = None
        uicontroller.update_control_text()
    

    reload_timer(player,uicontroller.cooldown_text)


    #update minimap and player position
    update_player_icon.minimap_update()
    minimap_icons.player_icon.rotation_z = player.rotation_y + 90

    #moving block for testing
    
    if enable_moving_block:
        global speed123
        global multi
        speed123 = 5 * time.dt * multi 
        moving_block.position += Vec3(speed123,0,0)
        if moving_block.intersects():
            multi *= -1
        if player.bullet_trail is not None:
            if player.bullet_trail.intersects(moving_block):
                audio_controller.success.play()
        update_moving_square_icon.minimap_update()
    

    #Runs once when you die
    if test:
        test = False
        death_manager.kill()
    #Continuiesly runs when you are dead
    if player.dead and not 5 < abs(time.perf_counter()-player.death_timer):
        death_manager.while_dead()
    #Runs once when you respawn
    elif player.dead:
        death_manager.respawned()


    #use this for taking a overview screenshot
    '''
    camera.position = (0, 100, 0)
    camera.rotation = (90, 0, 0) 
    '''
app.run()
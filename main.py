"""
This is the main file that will run the game
"""
#pylint: disable=redefined-builtin, wildcard-import

import logging
import time
import pathlib
import subprocess
from socket import gethostname, gethostbyname
from sys import executable
from atexit import register

from ursina import *
from ursina.networking import *

from scripts.game.controls import *
from scripts.game.player import get_player
from scripts.game.death import DeathManager
from scripts.game.minimap import UpdateMinimap, MinimapIcons
from scripts.game.combat import shoot, reload_timer, laser, update_laser
from scripts.game.audio_controller import AudioController
from scripts.game.settings import *
from scripts.game.ui import UIController
from scripts.game.shop import ShopUpgrades
from scripts.game.game_objective import KOTH
from scripts.game.main_menu import MainMenu
from scripts.game.chat import ChatController
from scripts.game.start_game import start_game, destory_all_cameras, end_round, buy_phase, start_round, end_game

from scripts.client.client_to_server import send_info, info_key
from scripts.client.parsing import parse_state
from scripts.client.rpc_functions import GameState, peer, state_to_client, game, on_connect, on_disconnect #pylint: disable=unused-import
#pylint: enable=redefined-builtin, wildcard-import

#Moving block for testing
moving_block = Entity(model="cube", color = color.yellow, position=(0,4,3),collider = "box", scale = (1,5,1))
speed123 = 5*time.dt
multi = 1
enable_moving_block = True
test = False
#Declare logging
logging.basicConfig(level=logging.DEBUG, format="(%(asctime)s) %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

#Create app
app = Ursina(icon="assets/textures/ursina.ico")

#Objects on the map
#grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y=1, collider ="box")
#yoru = Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="test123",rotation_x=0, y=0, collider = "box")
player_shadow = Entity(model="Better_Tank", color=color.red,rotation_x=0, y=0, enabled = False, scale = 0.5)
#cube = Entity(model='sphere', color=hsv(300,1,1), scale=5, collider='box')
cube1 = Entity(model='cube',scale=1, collider='box',position= (10,10,10),texture='test123')
center = Entity(model='cube',scale=1, collider='box',position= (0,0,0), texture = 'test123')

#Walls
wall1 = Entity(model="cube", scale=(50,12,0.3), color=color.red, collider = "box", x=0, z=-25)
wall2 = Entity(model="cube", scale=(50,12,0.3), color=color.green, collider = "box", x=0, z=25)
wall3 = Entity(model="cube", scale=(50,12,0.3), color=color.blue, collider = "box", x=-25, z=0, rotation_y=90)
wall4 = Entity(model="cube", scale=(50,12,0.3), color=color.black, collider = "box", x=25, z=0, rotation_y=90)
wall10 = Entity(model="cube", scale=(50,12,0.3), color=color.red, collider = "box", x=0, z=-26)
wall20 = Entity(model="cube", scale=(50,12,0.3), color=color.green, collider = "box", x=0, z=26)
wall30 = Entity(model="cube", scale=(50,12,0.3), color=color.blue, collider = "box", x=-26, z=0, rotation_y=90)
wall40 = Entity(model="cube", scale=(50,12,0.3), color=color.black, collider = "box", x=26, z=0, rotation_y=90)




#Setup
player = get_player()
player.collider = "box"
player.cd = time.perf_counter()
player_shadow.collider = MeshCollider(player_shadow, mesh = player_shadow.model)
player.previous_x = player.x
player.previous_y = player.y
ui_controller = UIController(player,mouse)
audio_controller = AudioController(player)
shop_upgrades = ShopUpgrades(player,ui_controller,audio_controller)
koth1 = KOTH(player,10,10,10,ui_controller,audio_controller)
chat = ChatController(player,ui_controller,audio_controller)
server_process:None|subprocess.Popen = None #pylint: disable=invalid-name
laser(player)
local_ip = gethostbyname(gethostname())

#Sets kill_server() on exit
@register
def kill_server() -> None:
    '''Kills the server process if it's open'''
    peer.disconnect_all()
    if server_process is not None:
        logger.info("Killing server...")
        server_process.kill()


    '''
    if player.current_cam == len(player.perspective_list) and player.in_round:
        player.current_cam = 1
        #If the camera is on the player and there is at least one camera
    elif player.current_cam == 0 and player.in_round:
        player.current_cam += 1
    '''

def cam_switching():
    '''Function for camera switching'''
    if player.current_cam == len(player.perspective_list):
        player.current_cam = 0
        #If the camera is on the player and there is at least one camera

    if player.current_cam == len(player.perspective_list) and player.in_round:
            player.current_cam = 1
            #If the camera is on the player and there is at least one camera
    elif player.current_cam == 0 and player.in_round:
            player.current_cam += 1

    if player.current_cam == 0 and len(player.perspective_list) > 1: #player
        player.in_camera = False
        ui_controller.camoverlay.disable()
        player.perspective_list[-1].visible = True
        camera.parent = player.camera_pivot
    elif player.current_cam != 0:
        camera.parent = player.perspective_list[player.current_cam].camera_pivot
        player.perspective_list[player.current_cam].visible = False
        player.perspective_list[player.current_cam-1].visible = True
        player.in_camera = True
        ui_controller.camoverlay.enable()
        ui_controller.camoverlay.text= f'cam {player.current_cam}'


#Variable declarations
player.perspective_list = [player]
minimap_icons = MinimapIcons(player)
death_manager = DeathManager(player, audio_controller, ui_controller, player_shadow,cam_switching)
update_player_icon = UpdateMinimap(minimap_icons.player_icon,player,55)
update_moving_square_icon = UpdateMinimap(minimap_icons.square_icon,moving_block,55)
main_menu = MainMenu(player,audio_controller,ui_controller)
main_menu.open_main_menu()

#Shop menu buttons
ui_controller.upgrade_cams_button.on_click = shop_upgrades.cam_upgrade
ui_controller.faster_reload_button.on_click = shop_upgrades.reload_upgrade

#Escape menu buttons
ui_controller.quit_button.on_click = main_menu.open_main_menu
ui_controller.volume_button.on_click = ui_controller.open_volume_menu
ui_controller.control_button.on_click = ui_controller.open_control_menu
ui_controller.resume_button.on_click = ui_controller.close_all_uis


#Main menu buttons
ui_controller.exit_game_button.on_click = main_menu.normal_exit
ui_controller.open_game_button.on_click = Sequence(Func(main_menu.enter_game), Wait(0.01), Func(cam_switching))
ui_controller.host_game_button.on_click = main_menu.open_host_game
ui_controller.map_selector_button.on_click = main_menu.open_map_selector
ui_controller.back_to_main_button.on_click = main_menu.exit_subscreen
ui_controller.name_input.on_click = Func(ui_controller.reset_input_field, ui_controller.name_input)

#Host server
def start_server() -> None:
    '''Start a local server'''
    #Removing the global would make the code more complicated
    global server_process #pylint: disable=global-statement
    port = ui_controller.port_input.text
    window_state_box_checked = ui_controller.has_window_checkbox.value
    if window_state_box_checked:
        window_state = "--window"
    else:
        window_state = "--no-window"
    if "__compiled__" in globals():
        #Code if compiled with nuitka
        #Assume multidist was used
        path = pathlib.Path(__file__).resolve()
        server_process = subprocess.Popen([path, "server", "--port", port, window_state])
    else:
        #Ran from source
        server_process = subprocess.Popen([executable, "server.py", "--port", port, window_state])
    #Auto connect if box is checked
    if ui_controller.auto_join_checkbox.value:
        peer.start("localhost", port, is_host=False)
        if not peer.is_running():
            logger.info("Server connection unsucessful")
        else:
            logger.info("Server sucessfully joined")

ui_controller.server_text.text = f"If you are connecting with someone on the same network, connect with hostname {local_ip}!"
ui_controller.start_server_button.on_click_setter(start_server)

#Join Server
def join_game() -> None:
    '''Function that connects to the server in the text fields'''
    host = ui_controller.host_input.text
    port = int(ui_controller.port_input.text)
    logger.debug("host: %s, port %d", host, port)
    try:
        logger.info("Attempted to join server")
        peer.start(host, port, is_host=False)
        if not peer.is_running():
            logger.info("Server connection unsucessful")
        else:
            logger.info("Server sucessfully joined")
    except Exception as err:
        logger.error(err)

ui_controller.join_friend_button.on_click = main_menu.open_join_game
ui_controller.port_input.on_click = Func(ui_controller.reset_input_field, ui_controller.port_input)
ui_controller.host_input.on_click = Func(ui_controller.reset_input_field, ui_controller.host_input)
ui_controller.join_game_button.on_click_setter(join_game)

#Control change buttons
ui_controller.reset_controls_to_default_button.on_click = ui_controller.reset_and_update_controls

#Functions to change the volume
def gun_change_volume():
    audio_controller.set_gun_volume(ui_controller.gun_volume_slider.value)

def player_change_volume():
    audio_controller.set_player_volume(ui_controller.player_volume_slider.value)

#Sound sliders
ui_controller.gun_volume_slider.on_value_changed = gun_change_volume
ui_controller.player_volume_slider.on_value_changed = player_change_volume

#Detect key inputs
def input(key):
    '''Input handler'''
    global test
     #Escape menu
    if player.in_main_menu:
        return

    if key == get_binding(Controls.QUIT_GAME) and not player.in_shop:
        player.in_menu = not player.in_menu
        player.in_chat = False
        ui_controller.chat_field.enabled = False
        #Buttons
        if player.in_menu:
            ui_controller.set_mouse_menu_state()
            ui_controller.ui_changer(True)
            ui_controller.menu_overlay.enabled = True
        else:
            ui_controller.set_mouse_game_state()
            ui_controller.open_volume_menu(False)
            ui_controller.open_control_menu(False)

    if key == get_binding(Controls.QUIT_GAME) and player.in_shop:
        player.in_shop = False
        ui_controller.open_shop_menu(False)

    if player.control_change_button_pressed:
        if isinstance(key, str) and "mouse" not in key and "escape" not in key:
            player.changed_key = key
            player.control_change_button_pressed = False

    if not player.input_enabled:
        return

    #Chat
    if key == get_binding(Controls.OPEN_CHAT) and not player.in_chat:
        ui_controller.chat_field.enabled = True
        print(vars(ui_controller.chat_field))
        print("hi")
        player.in_chat = True
        audio_controller.footsteps.stop()
        ui_controller.set_mouse_menu_state()
        ui_controller.chat_field.text = ""
        player.chat_opened = time.perf_counter()
        invoke(setattr, ui_controller.chat_field, "text", "", delay=0.01)        

    if key == get_binding(Controls.SEND_MSG) and player.in_chat:
        ui_controller.set_mouse_game_state()
        player.in_chat = False
        ui_controller.chat_field.enabled = False
        player.message = (Text(text = f"{player.username}: {ui_controller.chat_field.text}",
                              origin = (0.8,0),
                              position = (0.8,0,-2),
                              scale = 0.75,
                              color=color.white,
                              enabled = True))
        chat.chat_list.append(player.message)

    if player.in_chat:
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
        print(send_info(player))
        print(info_key())

    #Reset cameras
    if key == get_binding(Controls.RESET_CAMERAS) and player.in_shop:
        destory_all_cameras(player,ui_controller)

    #Placing camera
    if key == get_binding(Controls.PLACE_CAMERA) and not player.in_menu and not player.in_shop and not len(player.perspective_list) > player.max_cams:
        infront = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player, player.laser, player.bullet_trail] + player.perspective_list)
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
                cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = temp_cam.x/55,
                                  y= temp_cam.z/55, model = "quad", texture = "camera_icon", scale = 0.05)
                player.cam_icon_list.append(cam_icon)
        
    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)

    #Jumping sound
    if key == get_binding(Controls.JUMP) and player.grounded:
        audio_controller.jump.play()

    #Open shop menu
    if key == get_binding(Controls.OPEN_SHOP) and not player.in_menu and player.in_buy_phase:
        player.in_shop = not player.in_shop
        if player.in_shop:
            ui_controller.open_shop_menu(True)
        else:
            ui_controller.open_shop_menu(False)


    if key ==  "t":
        print(send_info(player))
        print(parse_state(send_info(player)))
        print(info_key())
        koth1.location_z = -10
        koth1.objective_length = 3
        koth1.update_zone()
        start_round(player,ui_controller)
        cam_switching()

def update():
    global test
    if peer.is_running():
        #Conected to multiplayer
        peer.update()
        if GameState.game_started:
            #In Game
            pass
        else:
            #Before game start
            pass

    if player.in_main_menu:
        return

    if player.in_chat:
        player.chat_opened = time.perf_counter()
    chat.chat()

    if player.in_round:
        ui_controller.round_timer_text.text = "Round ends in " + str (round((30 -(abs(time.perf_counter() - player.round_timer))),0))
        ui_controller.round_timer_text.enable()
        player.laser.enable()


    if player.in_round and 30 < abs(time.perf_counter() - player.round_timer):
        buy_phase(player, ui_controller, True)
        ui_controller.round_timer_text.disable()
        player.laser.disable()
        end_round(player,ui_controller)

    if player.in_buy_phase:
        ui_controller.shop_timer_text.text = "Buy phase ends in " + str (round((10 -(abs(time.perf_counter() - player.shop_timer))),0))
    
    if player.in_buy_phase and 10 < abs(time.perf_counter() - player.shop_timer):
        start_round(player,ui_controller)
        buy_phase(player, ui_controller, False)
        cam_switching()
        print(player.cash)
        
        

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
    koth1.within_zone()
    koth1.gain_points()


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
        ui_controller.update_control_text()

    reload_timer(player,ui_controller.cooldown_text)


    #update minimap and player position
    #some of this code is broken
    update_player_icon.minimap_update()
    minimap_icons.player_icon.rotation_z = player.rotation_y + 90
    '''
    minimap_icons.vision_cone_icon1.rotation_z = minimap_icons.player_icon.rotation_z - 135
    minimap_icons.vision_cone_icon.rotation_z = minimap_icons.player_icon.rotation_z - 55
    minimap_icons.vision_cone() 
    minimap_icons.in_sight(moving_block, camera)
    '''
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

    update_laser(player)

    if player.in_chat == True:
        return

    if held_keys[get_binding(Controls.CHECK_LEADERBOARD)] and not player.in_menu and not player.in_shop:
        ui_controller.toggle_leaderboard(True)
    else:
        ui_controller.toggle_leaderboard(False)

    if held_keys[get_binding(Controls.CAMERA_LEFT)]:
        player_shadow.rotation_y -= player_sensitivity * time.dt

    if held_keys[get_binding(Controls.CAMERA_RIGHT)]:
        player_shadow.rotation_y += player_sensitivity * time.dt
    #use this for taking a overview screenshot
    '''
    camera.position = (0, 100, 0)
    camera.rotation = (90, 0, 0) 
    '''
app.run()
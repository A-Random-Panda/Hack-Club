"""
This is the main file that will run the game
"""
#pylint: disable=redefined-builtin, wildcard-import

import logging
import time
import subprocess
import os
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
from scripts.game.start_game import reset_values, destory_all_cameras, end_round, buy_phase, start_round, end_game, set_spawn

from scripts.client.client_to_server import send_info, info_key
from scripts.client.parsing import parse_state
from scripts.client.rpc_functions import * #pylint: disable=unused-import
from maps.map_purgatory import Purgatory
#pylint: enable=redefined-builtin, wildcard-import

#Declare logging
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(levelname)s - %(message)s", filemode='w', filename="latest.log", encoding="utf-8")
logger = logging.getLogger(__name__)

application.asset_folder = Path(__file__).parent / "assets"

#Create app
app = Ursina(icon="assets/textures/ursina.ico", development_mode=False, borderless=True, fullscreen=True, forced_aspect_ratio = 16/9)

Purgatory.load_map()
player_shadow = Entity(model="tank",rotation_x=0, y=0, enabled = False, scale = 0.5,texture="bluetest")
player_enemy = Entity(model="tank",rotation_x=0, y=1.5, enabled = True, scale = 0.5,texture="dom")

#Setup
player = get_player()
player.position = (7,1,7)
player.collider = MeshCollider(player, mesh = player.model)
player_enemy.collider = MeshCollider(player_enemy, mesh = player_enemy.model)
player.cd = time.perf_counter()
player.previous_x = player.x
player.previous_y = player.y
ui_controller = UIController(player,mouse)
audio_controller = AudioController(player)
shop_upgrades = ShopUpgrades(player,ui_controller,audio_controller)
koth1 = KOTH(player,10,0,0,ui_controller,audio_controller)
chat = ChatController(ui_controller,audio_controller)
laser(player)
server_process:None|subprocess.Popen = None #pylint: disable=invalid-name
local_ip = gethostbyname(gethostname())

#Sets kill_server() on exit
@register
def kill_server() -> None:
    '''Kills the server process if it's open'''
    if server_process is not None:
        logger.info("Killing server...")
        if os.name == "nt":
            print("taskkill", "/F", "/T", "PID", str(server_process.pid))
            subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(server_process.pid)])
        elif os.name == "posix":
            os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)

@register
def disconnect() -> None:
    '''Ensures that the server gets the disconnect symbol when the game closes'''
    peer.disconnect_all()

def cam_switching(in_buy = False):
    '''Function for camera switching'''
    if player.current_cam == len(player.perspective_list) or in_buy:
        player.current_cam = 0
        #If the camera is on the player and there is at least one camera

    if player.current_cam == len(player.perspective_list) and player.in_round:
            player.current_cam = 1
            #If the camera is on the player and there is at least one camera
    elif player.current_cam == 0 and player.in_round:
            player.current_cam += 1

    if (player.current_cam == 0 and len(player.perspective_list) > 1) or in_buy: #player
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

def complete_reset():
    '''Completely resets the game'''
    print("Current screen: ", main_menu.current_screen)
    main_menu.exit_subscreen()
    main_menu.open_main_menu()
    reset_values(player,ui_controller)
    first_cam = Entity(model = 'cypher_cam',
                                    position = (0,3,0),
                                    texture = "cam",
                                    rotation = (180,90,180))
    cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = first_cam.x/MINIMAP_X,
                                      y= first_cam.z/MINIMAP_Y, model = "quad", texture = "camera_icon", scale = 0.05, color = color.blue)
    player.cam_icon_list.append(cam_icon)
    first_cam.camera_pivot = Entity(parent=first_cam, y = 1.6)
    first_cam.original_rotation_y = first_cam.rotation_y
    first_cam.collider = MeshCollider(first_cam, mesh = first_cam.model)
    player.perspective_list.append(first_cam)
    ui_controller.set_mouse_menu_state()

def multiplayer_leave_wrapper():
    '''
    Wrapper to check if you're connected to a server when you go to the main menu,
    and disconnect if you are
    '''
    if peer.is_running():
        peer.disconnect_all()

#Variable declarations
player.perspective_list = [player]
minimap_icons = MinimapIcons(player)
death_manager = DeathManager(player, audio_controller, ui_controller, player_shadow,cam_switching)
update_player_icon = UpdateMinimap(minimap_icons.player_icon,player,MINIMAP_X,MINIMAP_Y)
main_menu = MainMenu(player,audio_controller,ui_controller)

#Sets ui controller and main menu in rpc functions
GameState.set_ui_controller(ui_controller)
GameState.set_main_menu(main_menu)
GameState.set_chat(chat)
GameState.set_reset_function(complete_reset)

main_menu.open_main_menu()

#Shop menu buttons
ui_controller.upgrade_cams_button.on_click_setter(shop_upgrades.cam_upgrade)
ui_controller.faster_reload_button.on_click_setter(shop_upgrades.reload_upgrade)

#Escape menu buttons
ui_controller.quit_button.on_click_setter(Sequence(complete_reset, multiplayer_leave_wrapper))
ui_controller.volume_button.on_click_setter(ui_controller.open_volume_menu)
ui_controller.control_button.on_click_setter(ui_controller.open_control_menu)
ui_controller.resume_button.on_click_setter(ui_controller.close_all_uis)

#Main menu buttons
ui_controller.exit_game_button.on_click_setter(main_menu.normal_exit)
ui_controller.open_game_button.on_click_setter(Sequence(Func(main_menu.enter_game), Wait(0.01), Func(cam_switching)))
ui_controller.host_game_button.on_click_setter(main_menu.open_host_game)
ui_controller.rules_button.on_click_setter(main_menu.open_rules_menu)
ui_controller.lobby_botton.on_click_setter(main_menu.open_lobby)
ui_controller.back_to_main_button.on_click_setter(main_menu.exit_subscreen)
ui_controller.name_input.on_click_setter(Func(ui_controller.reset_input_field, ui_controller.name_input))

#Host server
def start_server() -> None:
    '''Start a local server'''
    #Removing the global would make the code more complicated
    global server_process #pylint: disable=global-statement
    if server_process is not None:
        #Should probably put a text box and kill the server but who cares
        ui_controller.show_temp_text("""A server has already been started.
        If you want to restart the server, stop the server than start it again""", delay=3)
        return
    ui_controller.show_temp_text("Starting server...")
    port = ui_controller.port_input.text
    window_state_box_checked = ui_controller.has_window_checkbox.value
    if window_state_box_checked:
        window_state = "--window"
    else:
        window_state = "--no-window"
    if "__compiled__" in globals():
        #Code if compiled with nuitka
        logger.info("Server started")
        with open ("latest-server.log", "w", encoding="utf-8") as log:
            server_process = subprocess.Popen(["server.exe", "--port", port, window_state],
                                            stdout=log,
                                            stderr=subprocess.DEVNULL,
                                            start_new_session=True
                                            )
    else:
        #Ran from source
        server_process = subprocess.Popen([executable, "server.py", "--port", port, window_state],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL,
                                           start_new_session=True
                                           )
    #Auto connect if box is checked
    if ui_controller.auto_join_checkbox.value:
        peer.start("localhost", port, is_host=False)

ui_controller.server_text.text = f"If you are connecting with someone on the same network, connect with hostname {local_ip}!"
ui_controller.start_server_button.on_click_setter(start_server)

#Join Server
def join_game() -> None:
    '''Function that connects to the server in the UI'''
    host = ui_controller.host_input.text
    port = int(ui_controller.port_input.text)
    logger.debug("host: %s, port %d", host, port)
    try:
        logger.info("Attempted to join server")
        peer.start(host, port, is_host=False)
        ui_controller.show_temp_text("Connecting... This may take a while")
    except Exception:
        ui_controller.show_temp_text("You failed to join the server")

ui_controller.join_friend_button.on_click_setter(main_menu.open_join_game)
ui_controller.port_input.on_click_setter(Func(ui_controller.reset_input_field, ui_controller.port_input))
ui_controller.host_input.on_click_setter(Func(ui_controller.reset_input_field, ui_controller.host_input))
ui_controller.join_game_button.on_click_setter(join_game)

#Lobby
def start_multiplayer_game() -> None:
    '''Tells the server to start the game'''
    if not peer.is_running():
        ui_controller.show_temp_text("You are not connected to a server.")
        return
    if ui_controller.lobby_text.text.count("\n") < 2:
        ui_controller.show_temp_text("There are not enough people in the server to start the game.")
        return
    try:
        peer.start_game(peer.get_connections()[0])
    except Exception as err:
        logger.error("%s when trying to start game", err)

def disconnect_from_server() -> None:
    '''Disconnects from the server if connected'''
    if peer.is_running():
        peer.disconnect_all()
        #ui_controller.show_temp_text("You left the server")
    else:
        ui_controller.show_temp_text("You were not connected to a server")

def stop_server() -> None:
    global server_process #pylint: disable=global-statement
    if server_process is not None:
        kill_server()
        server_process = None
        ui_controller.show_temp_text("The server was stopped.")
    else:
        ui_controller.show_temp_text("A server was not already started.")

ui_controller.start_game_button.on_click_setter(start_multiplayer_game)
ui_controller.disconnect_button.on_click_setter(disconnect_from_server)
ui_controller.stop_server_button.on_click_setter(stop_server)

#Control change buttons
ui_controller.reset_controls_to_default_button.on_click_setter(ui_controller.reset_and_update_controls)

#Functions to change the volume
def gun_change_volume():
    audio_controller.set_gun_volume(ui_controller.gun_volume_slider.value)
    ui_controller.save_settings()

def player_change_volume():
    audio_controller.set_player_volume(ui_controller.player_volume_slider.value)
    ui_controller.save_settings()

#Sound sliders
ui_controller.gun_volume_slider.on_value_changed = gun_change_volume
ui_controller.player_volume_slider.on_value_changed = player_change_volume

#Starter Cam
first_cam = Entity(model = 'cypher_cam',
                                position = (0,3,0),
                                texture = "cam",
                                rotation = (180,90,180))
cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = first_cam.x/MINIMAP_X,
                                  y= first_cam.z/MINIMAP_Y, model = "quad", texture = "camera_icon", scale = 0.05, color=color.blue)
player.cam_icon_list.append(cam_icon)
first_cam.camera_pivot = Entity(parent=first_cam, y = 1.6)
first_cam.original_rotation_y = first_cam.rotation_y
first_cam.collider = MeshCollider(first_cam, mesh = first_cam.model)
player.perspective_list.append(first_cam)

#Detect key inputs
def input(key):
    '''Input handler'''
    if key == '0':
        print(ui_controller.temp_text.text)
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
        player.in_chat = True
        audio_controller.footsteps.stop()
        ui_controller.set_mouse_menu_state()
        ui_controller.chat_field.text = ""
        chat.start_chat_timer()
        invoke(setattr, ui_controller.chat_field, "text", "", delay=0.01)

    if key == get_binding(Controls.SEND_MSG) and player.in_chat:
        ui_controller.set_mouse_game_state()
        player.in_chat = False
        ui_controller.chat_field.enabled = False
        if peer.is_running():
            peer.chat_to_server(peer.get_connections()[0], f"{player.username}: {ui_controller.chat_field.text}")
        else:
            chat.chat_list.append(Text(text = f"{player.username}: {ui_controller.chat_field.text}",
                              origin = (0.8,0),
                              position = (0.8,0,-2),
                              scale = 0.75,
                              color=color.white,
                              enabled = True))

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

    #Reset cameras
    if key == get_binding(Controls.RESET_CAMERAS) and player.in_buy_phase:
        destory_all_cameras(player,ui_controller)
        first_cam = Entity(model = 'cypher_cam',
                                position = (0,3,0),
                                texture = "cam",
                                rotation = (180,90,180))
        cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = first_cam.x/MINIMAP_X,
                                  y= first_cam.z/MINIMAP_Y, model = "quad", texture = "camera_icon", scale = 0.05, color = color.blue)
        player.cam_icon_list.append(cam_icon)
        first_cam.camera_pivot = Entity(parent=first_cam, y = 1.6)
        first_cam.original_rotation_y = first_cam.rotation_y
        first_cam.collider = MeshCollider(first_cam, mesh = first_cam.model)
        player.perspective_list.append(first_cam)

    #Placing camera
    if key == get_binding(Controls.PLACE_CAMERA) and not player.in_menu and not player.in_shop and not len(player.perspective_list) > player.max_cams:
        infront = raycast(camera.world_position, camera.forward, distance = 5, ignore = [player, player.laser, player.bullet_trail, player_enemy] + player.perspective_list)
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
                cam_icon = Entity(parent = minimap_icons.minimap, z = -.4, x = temp_cam.x/MINIMAP_X,
                                  y= temp_cam.z/MINIMAP_Y, model = "quad", texture = "camera_icon", scale = 0.05, color = color.blue)
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

def update():
    if peer.is_running():
        #Conected to multiplayer
        peer.update()
        if GameState.opponent_disconnected:
            GameState.game_started = False
            GameState.opponent_disconnected = False
            ui_controller.show_temp_text("Your opponent has disconnected", delay=3)
        if GameState.game_started:
            #Multiplayer code
            if GameState.state_string:
                state = parse_state(GameState.state_string)
                if not player.game_begin:
                    buy_phase(player,ui_controller)
                    player.game_begin = True
                    if state["opponent_id"] > GameState.id:
                        player.world_position = RESPAWN_POINTS[0]
                        player.rotation_y = RESPAWN_ROTATION[0]
                    else:
                        player.world_position = RESPAWN_POINTS[1]
                        player.rotation_y = RESPAWN_ROTATION[1]
                player_enemy.world_position_setter(state["world_pos"])
                player_enemy.rotation_setter(state["player_rotation"])

                if player.bullet_trail is not None and not player.in_buy_phase:
                    if player.bullet_trail.intersects(player_enemy):
                        audio_controller.hit_conf.play()
                        player.cash += 200
                        player.shot_someone = True
                        ui_controller.kill_png.enable()
                        invoke(setattr, ui_controller.kill_png, "enabled", False, delay = 5)
    
                if player.in_round:
                    ui_controller.round_timer_text.text = "Round ends in " + str (round((180 -(time.perf_counter() - player.round_timer)),0))
                    ui_controller.round_timer_text.enable()
                    player.laser.enable()
                    player_enemy.enabled = True


                if player.in_round and 180 < (time.perf_counter() - player.round_timer):
                    buy_phase(player, ui_controller, True)
                    ui_controller.round_timer_text.disable()
                    player.laser.disable()
                    cam_switching(True)
                    end_round(player,ui_controller, state["points"])
                    if player.round_wins == 7 and not player.game_over:
                        ui_controller.menu_overlay.enable()
                        ui_controller.game_win.enable()
                        invoke(reset_values, player, ui_controller, state["opponent_id"], GameState.id, delay = 10)
                        invoke(set_spawn, player, state["opponent_id"], GameState.id, delay = 10)
                        player.game_over == True
                    elif state["round_wins"] == 7 and not player.game_over:
                        ui_controller.menu_overlay.enable()
                        ui_controller.game_lose.enable()
                        invoke(reset_values, player, ui_controller, state["opponent_id"], GameState.id, delay = 10)
                        invoke(set_spawn, player, state["opponent_id"], GameState.id, delay = 10)
                        player.game_over == True

                if player.in_buy_phase:
                    ui_controller.shop_timer_text.text = "Buy phase ends in " + str (round((30 -(abs(time.perf_counter() - player.shop_timer))),0))
                    player_enemy.enabled = False
                    
                if player.in_buy_phase and 30 < abs(time.perf_counter() - player.shop_timer):
                    start_round(player,ui_controller,state["opponent_id"],GameState.id)
                    buy_phase(player, ui_controller, False)
                    cam_switching()
                if state["is_shooting"] and player.enemy_shot and not player.in_buy_phase:
                    enemy_bullet_trail = Entity(model="cube",
                                                        position= state["bullet_pos"],
                                                        scale = state["bullet_scale"],
                                                        color = color.white,parent = scene,
                                                        rotation = state["player_rotation"],
                                                        collider = "box"
                                                        )
                    audio_controller.shooting.play()
                    player.enemy_shot = False
                    destroy(enemy_bullet_trail,delay = 0.1)
                    invoke(setattr, player, "enemy_shot", True, delay = 0.1)
                koth1.within_zone()
                if not state["in_zone"] and not player.in_buy_phase and player.in_zone:
                    koth1.gain_points(state["points"],GameState.opponent_name,state["round_wins"])
                    ui_controller.contested_text.enabled = False
                elif not state["in_zone"] and player.in_zone:
                    ui_controller.contested_text.enabled = False
    
                if state["in_zone"] and player.in_zone and not player.in_buy_phase:
                    if not ui_controller.contested_text.enabled:
                        ui_controller.contested_text.enabled = True
                elif state["in_zone"]:
                    ui_controller.enemy_leaderboard_text.text = f"{state["points"]} {GameState.opponent_name.replace(player.username, "")} \n round wins: {state["round_wins"]}"
                
                if state["shot_someone"] and not player.in_buy_phase:
                    death_manager.kill()
                if state["is_dead"]:
                    player_enemy.disable()
                    player.shot_someone = False
                    invoke(setattr, player, "enabled", True, delay = 5)
                #Continuiesly runs when you are dead
                if player.dead and not 5 < abs(time.perf_counter()-player.death_timer) and not player.in_buy_phase:
                    death_manager.while_dead()
                    #Runs once when you respawn
                elif player.dead:
                    death_manager.respawned()
                

                
            #In Game
            try:
                peer.state_to_server(peer.get_connections()[0], send_info(player))
            except Exception as err:
                logger.error("%s: Error while trying to send state to server", err)
        else:
            #Before game start
            pass

    if player.in_main_menu:
        return

    if player.in_chat:
        chat.start_chat_timer()
    chat.chat()



    if player.y < -2:
        player.position = (7, 1.0,7)

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

    #moving block for testing

    update_laser(player)

    if player.in_chat:
        return

    if held_keys[get_binding(Controls.CHECK_LEADERBOARD)] and not player.in_menu and not player.in_shop:
        ui_controller.toggle_leaderboard(True)
    else:
        ui_controller.toggle_leaderboard(False)

    if held_keys[get_binding(Controls.CAMERA_LEFT)]:
        player_shadow.rotation_y -= player_sensitivity * time.dt

    if held_keys[get_binding(Controls.CAMERA_RIGHT)]:
        player_shadow.rotation_y += player_sensitivity * time.dt
    #use this for taking a overview screenshot for the minimap
    '''
    camera.position = (0, 100, 0)
    camera.rotation = (90, 0, 0) 
    player_enemy.disable()
    if held_keys["t"]:
        player.cursor.enabled = False
    '''
app.run()
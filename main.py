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
from scripts.minimap import UpdateMinimap
from scripts.combat import shoot, reload_timer
from scripts.audio_controller import AudioController

#Moving block for testing
moving_block = Entity(model="cube", color = color.yellow, position=(0,4,3),collider = "box", scale = (1,5,1))
speed123 = 5*time.dt
multi = 1
enable_moving_block = True
test = False
#Declare logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Upgrade cost list (place holders)
MAX_CAM_COST = [100,500,1500,4500,7000]
FASTER_RELOAD_COST = [100,500,1500,4500,7000]

#Settings
player_sensitivity = 150
player_volume = 1.5


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
camoverlay = Text (parent = camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
camoverlay.disable()
player = get_player()
player.visible = False
player.cd = time.perf_counter()
player.collider = MeshCollider(player, mesh = player.model)
player.previous_x = player.x
player.previous_y = player.y
cooldown_text = Text("test", origin = (0,0),position = (-.6,-.4,-.9), scale = 1.5, color=color.green,enabled = True)
text_box = Entity(scale = (0.4,0.1) ,origin = (0,0), position = (-.6,-.4), parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), enabled = True)
menu_overlay = Entity(scale = (2,2) , parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)
current_cash = Text(f"{player.cash} cash", origin = (0,0), position = (-.7,.4,-2), scale = 1, enabled = False)
respawn_text = Text("test", origin = (0,0),position = (0,0,-2), scale = 3, color=color.red,enabled = False)
#mini map
minimap = Entity(scale=(0.2,0.2), x = 0.7, y= 0.4, model = "quad", texture="map_1", parent = camera.ui)
player_icon = Entity(parent = minimap, texture = "red_dot", scale = 0.05, model = "quad", z =-0.5, color=color.red)
vision_cone_icon = Entity(scale = (4,0.2), parent=player_icon, model = "quad", z = -1, color = color.red, origin = (0.7,0), a = 0.4 )
sqaure_icon = Entity(parent = minimap, scale = 0.05, model = "quad", z =-0.5)
    
#Function used to update variables to allow you to change controls
def control_changer(control,button):
    player.control_change_button_pressed = True
    player.control_change_key = control
    button.text = "Press a key to assign\n it to this action"


#Shop upgrade functions
def cam_upgrade():
    current_upgrade = player.max_cams-5
    if current_upgrade == len(MAX_CAM_COST)-1 and player.cash >= MAX_CAM_COST[current_upgrade]:
        player.cash -= MAX_CAM_COST[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        player.max_cams += 1
        upgrade_cams_button.text = f"current cams: {player.max_cams} \n MAXED OUT"
        audio_controller.success.play()
    elif current_upgrade < len(MAX_CAM_COST) and player.cash >= MAX_CAM_COST[current_upgrade]:
        player.cash -= MAX_CAM_COST[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        next_cost = MAX_CAM_COST[current_upgrade + 1]
        player.max_cams += 1
        upgrade_cams_button.text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${next_cost}"
        audio_controller.success.play()

def reload_upgrade():
    current_upgrade = int((5-player.reload_time)/0.5)
    if current_upgrade == len(FASTER_RELOAD_COST)-1 and player.cash >= FASTER_RELOAD_COST[current_upgrade]:
        player.cash -= FASTER_RELOAD_COST[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        player.reload_time -= 0.5
        faster_reload_button.text = f"reload time: {player.reload_time} \n MAXED OUT"
        audio_controller.success.play()
    elif current_upgrade < len(FASTER_RELOAD_COST) and player.cash >= FASTER_RELOAD_COST[current_upgrade]:
        player.cash -= FASTER_RELOAD_COST[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        next_cost = FASTER_RELOAD_COST[current_upgrade + 1]
        player.reload_time -= 0.5
        faster_reload_button.text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${next_cost}"
        audio_controller.success.play()

#Functions used to help Enter / Exist out of UIs

def ui_changer(boolean = False):
    for button in button_list:
        button.enabled = boolean
    for upgrades in shop_buttons_list:
        upgrades.enabled = False

def open_shop_menu(boolean = False):
    menu_overlay.enabled = boolean
    upgrade_cams_button.enabled = boolean
    faster_reload_button.enabled = boolean
    mouse.visible = boolean
    mouse.locked = not boolean
    player.cursor.enabled = not boolean
    current_cash.enabled = boolean


def open_volume_menu(boolean = True):
    ui_changer()
    menu_overlay.enabled = boolean
    gun_volume_slider.enabled = boolean
    player_volume_slider.enabled = boolean

def open_control_menu(boolean = True):
    ui_changer()
    menu_overlay.enabled = boolean
    for button in control_button_list:
        button.enabled = boolean




#Buttons in shop menu
upgrade_cams_button = Button(model = "quad", scale = 0.2, x = -0.1, z = -2, color=color.gray, text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${MAX_CAM_COST[0]}" , text_size = 0.8, text_color = color.black, enabled = False)
upgrade_cams_button.on_click = cam_upgrade
faster_reload_button = Button(model = "quad", scale = 0.2, x = 0.1, z = -2, color=color.gray, text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${FASTER_RELOAD_COST[0]}", text_size = 0.8, text_color = color.black, enabled = False)
faster_reload_button.on_click = reload_upgrade
shop_buttons_list = [upgrade_cams_button,faster_reload_button]

#Buttons in main menu
button_list = []

quit_button = Button(model = "quad", scale = 0.2, x = 0, z = -2, color=color.gray, text = "Quit Game", text_size = 0.8, text_color = color.black, enabled = False)
quit_button.on_click = application.quit

volume_button = Button(model = "quad", scale = 0.2, x = 0.2, z = -2, color = color.gray, text = "volume controls", text_size = 0.8, text_color = color.black, enabled = False)
volume_button.on_click = open_volume_menu

control_button = Button(model = "quad", scale = 0.2, x = -0.2, z = -2, color = color.gray, text = "controls", text_size = 0.8, text_color = color.black, enabled = False)
control_button.on_click = open_control_menu

button_list.extend([volume_button,quit_button,control_button])

#Buttons in control menu
control_button_list = []
control_buttons_dict = {}

#Creates the buttons and adds them to a list and dictionary
for name, control, x, y in control_button_data_list:
    button = Button(model = "quad",
                    scale = 0.2, x = x, y = y,z = -2,color = color.gray, text = f"{name} \n{get_binding(control)}",
                    text_size =0.8, text_color= color.black, enabled = False)
    button.name = name
    button.on_click = Func(control_changer, control,button)
    control_button_list.append(button)
    control_buttons_dict[control] = button

#Function used to reset controls
def reset_and_update_controls():
    reset_controls_to_default()
    update_control_text()

#Reset button (manuelly added)
reset_controls_to_default_button = Button(model = "quad", scale = 0.2, x = -0.8, y = 0.4,z = -2,color=color.gray,
                                        text = "Reset Keybinds", text_size = 0.8, text_color = color.black, enabled = False)
reset_controls_to_default_button.on_click = reset_and_update_controls
control_button_list.append(reset_controls_to_default_button)


#Update the control buttons text after it changes
def update_control_text():
    for control, button in control_buttons_dict.items():
        button.text = f'{button.name}\n{get_binding(control)}'

def cam_switching():
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

#Variable declarations
player.perspective_list = [player]
audio_controller = AudioController(player)
death_manager = DeathManager(player, menu_overlay, audio_controller, respawn_text, player_shadow,cam_switching)
update_player_icon = UpdateMinimap(player_icon,player,55)
update_moving_sqaure_icon = UpdateMinimap(sqaure_icon,moving_block,55)

#Functions to change the volume
def gun_change_volume():
    audio_controller.set_gun_volume(gun_volume_slider.value)

def player_change_volume():
    audio_controller.set_player_volume(player_volume_slider.value)

#Sliders
#All gun related sounds
gun_volume_slider = ThinSlider(text='Gun Volume',
                               dynamic=True, 
                               max = 100, 
                               step = 1, 
                               z = -2, 
                               x = -.25,
                               y = 0, 
                               enabled = False, 
                               default = 50, 
                               on_value_changed = gun_change_volume)
gun_volume_slider.label.origin = (0,0)
gun_volume_slider.label.position = (.25, -.05)

#All player sounds
player_volume_slider = ThinSlider(text='Footstep Volume', 
                                    dynamic=True, 
                                    max = 100, 
                                    z = -2, 
                                    step = 1, 
                                    x =-.25, 
                                    y=-.2, 
                                    enabled = False, 
                                    default = 50, 
                                    on_value_changed = player_change_volume)
player_volume_slider.label.origin = (0,0)
player_volume_slider.label.position = (.25, -0.06)

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
            ui_changer(True)
            menu_overlay.enabled = True
        else:
            mouse.visible = False
            mouse.locked = True
            player.cursor.enabled = True
            open_volume_menu(False)
            open_control_menu(False)
    
    if key == get_binding(Controls.QUIT_GAME) and player.in_shop:
        player.in_shop = False
        open_shop_menu(False)


    
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
        camoverlay.disable()
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
                cam_icon = Entity(parent = minimap, z = -.4, x = temp_cam.x/55,y= temp_cam.z/55, model = "quad", texture = "camera_icon", scale = 0.05)
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
            open_shop_menu(True)
        else:
            open_shop_menu(False)

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
        update_control_text()
    

    reload_timer(player,cooldown_text)


    #update minimap and player position
    update_player_icon.minimap_update()
    player_icon.rotation_z = player.rotation_y + 90

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
        update_moving_sqaure_icon.minimap_update()
    

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
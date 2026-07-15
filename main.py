"""
This is the main file that will run the game
"""
import logging
import socket
import time
from ursina import *
from scripts.controls import *
from scripts.player import get_player
from scripts.death import *
#Moving block for testing
moving_block = Entity(model="cube", color = color.yellow, position=(0,4,3),collider = "box", scale = (1,5,1))
speed123 = 5*time.dt
multi = 1
enable_moving_block = True
test = False
#Declare logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

#Upgrade cost list (place holders)
max_cam_cost = [100,500,1500,4500,7000]
faster_reload_cost = [100,500,1500,4500,7000]

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
camoverlay = Text (parent= camera.ui,scale=2,position=(-0.7,0.4),color=color.gray)
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
mini_map = Entity(scale=(0.2,0.2), x = 0.7, y= 0.4, model = "quad", texture="map_1", parent = camera.ui)
player_icon = Entity(parent = mini_map, texture = "red_dot", scale = 0.05, model = "quad", z =-0.5, color=color.red)
vision_cone_icon = Entity(scale = (4,0.2), parent=player_icon, model = "quad", z = -1, color = color.red, origin = (0.7,0), a = 0.4 )
sqaure_icon = Entity(parent = mini_map, scale = 0.05, model = "quad", z =-0.5)

#Initializing sounds
shooting = Audio("sniper_shot",autoplay=False, volume= 0.5, spatial = True)
shooting.parent = player
success = Audio("success",autoplay = False, volume = player_volume, spatial = True)
death = Audio("death",autoplay = False, volume = player_volume, spatial = True)
death.parent = player
foot_steps = Audio("foot_steps", autoplay = False, volume = 1, spatial = True)
jumping = Audio("jumping", autoplay = False, volume = 1, spatial = True)
sniper_reload = Audio("sniper_reload", autoplay = False, volume = 0.83, spatial = True)

#Stop all sounds
def stop_audio():
    for audio in scene.entities:
            if isinstance(audio, Audio):
                audio.stop()
    
    

#Function used to update variables to allow you to change controls
def control_changer(control,button):
    player.control_change_button_pressed = True
    player.control_change_key = control
    button.text = "Press a key to assign\n it to this action"

def position_to_icon():
    return player.position.x/55, player.position.z/55


#Shop upgrade functions
def cam_upgrade():
    current_upgrade = player.max_cams-5
    if current_upgrade == len(max_cam_cost)-1 and player.cash >= max_cam_cost[current_upgrade]:
        player.cash -= max_cam_cost[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        player.max_cams += 1
        upgrade_cams_button.text = f"current cams: {player.max_cams} \n MAXED OUT"
        success.play()
    elif current_upgrade < len(max_cam_cost) and player.cash >= max_cam_cost[current_upgrade]:
        player.cash -= max_cam_cost[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        next_cost = max_cam_cost[current_upgrade + 1]
        player.max_cams += 1
        upgrade_cams_button.text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${next_cost}"
        success.play()

def reload_upgrade():
    current_upgrade = int((5-player.reload_time)/0.5)
    if current_upgrade == len(faster_reload_cost)-1 and player.cash >= faster_reload_cost[current_upgrade]:
        player.cash -= faster_reload_cost[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        player.reload_time -= 0.5
        faster_reload_button.text = f"reload time: {player.reload_time} \n MAXED OUT"
        success.play()
    elif current_upgrade < len(faster_reload_cost) and player.cash >= faster_reload_cost[current_upgrade]:
        player.cash -= faster_reload_cost[current_upgrade]
        current_cash.text = f"{player.cash} cash"
        next_cost = faster_reload_cost[current_upgrade + 1]
        player.reload_time -= 0.5
        faster_reload_button.text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${next_cost}"
        success.play()

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
    footstep_volume_slider.enabled = boolean

def open_control_menu(boolean = True):
    ui_changer()
    menu_overlay.enabled = boolean
    for button in control_button_list:
        button.enabled = boolean


#Used to change volume
def gun_change_volume():
    shooting.volume = (gun_volume_slider.value/100)
    sniper_reload.volume = (gun_volume_slider.value/60)
def footsteps_change_volume():
    foot_steps.volume = (footstep_volume_slider.value/50)
    jumping.volume = (footstep_volume_slider.value/50)

#Sliders
gun_volume_slider = ThinSlider(text='Gun Volume', dynamic=True, max = 100, step = 1, z = -2, x = -.25,y = 0, enabled = False, default = 50, on_value_changed = gun_change_volume)
gun_volume_slider.label.origin = (0,0)
gun_volume_slider.label.position = (.25, -.05)

footstep_volume_slider = ThinSlider(text='Footstep Volume', dynamic=True, max = 100, z = -2, step = 1, x =-.25, y=-.2, enabled = False, default = 50, on_value_changed = footsteps_change_volume)
footstep_volume_slider.label.origin = (0,0)
footstep_volume_slider.label.position = (.25, -0.06)

#Buttons in shop menu
upgrade_cams_button = Button(model = "quad", scale = 0.2, x = -0.1, z = -2, color=color.gray, text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${max_cam_cost[0]}" , text_size = 0.8, text_color = color.black, enabled = False)
upgrade_cams_button.on_click = cam_upgrade
faster_reload_button = Button(model = "quad", scale = 0.2, x = 0.1, z = -2, color=color.gray, text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${faster_reload_cost[0]}", text_size = 0.8, text_color = color.black, enabled = False)
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
        play_multi = 1 / (player.reload_time / 5)
        if player.reload_time < abs(time.perf_counter()-player.cd):
            hit = raycast(origin = player.world_position + player.forward,distance=1000, direction = player.forward)
            player.cd = time.perf_counter()
            shooting.pitch = play_multi
            sniper_reload.pitch = play_multi
            Sequence(Func(shooting.play),
                     Wait(0.9 / play_multi),
                     Func(sniper_reload.play)).start()
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
                cam_icon = Entity(parent = mini_map, z = -.4, x = temp_cam.x/55,y= temp_cam.z/55, model = "quad", texture = "camera_icon", scale = 0.05)
                player.cam_icon_list.append(cam_icon)
        
    if key == get_binding(Controls.FREECAM_MODE): #freecam mode
        EditorCamera(enabled=True)

   
    #Jumping sound
    if key == get_binding(Controls.JUMP) and player.grounded:
        jumping.play()
    
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
    if player.x != player.previous_x and not foot_steps.playing and not player.y != player.previous_y:
        foot_steps.play()
    if (player.x == player.previous_x or not player.grounded) and foot_steps.playing:
        foot_steps.stop()
    player.previous_x = player.x
    player.previous_y = player.y
    
    #Changes controls
    if player.changed_key is not None:
        set_control(player.control_change_key, player.changed_key)
        player.changed_key = None
        update_control_text()
    


    timer = "Shooting cooldown " + str(round(player.reload_time - time.perf_counter() +player.cd, 1))
    cooldown_text.text = timer if player.reload_time - (time.perf_counter()-player.cd) > 0 else "READY"

    #update minimap and player position
    player_icon.x = position_to_icon()[0]
    player_icon.y = position_to_icon()[1]
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
                success.play()
        sqaure_icon.x = moving_block.x/55
        sqaure_icon.y = moving_block.y/55
    

    #Runs once when you die
    if test:
    #if player.bullet_trail and player.bullet_trail.intersects(player).hit: #uncomment when multiplayer is added
        stop_audio()
        death.play()
        player.enabled = False
        player.dead = True
        player.death_timer = time.perf_counter()
        print("dead")
        test = False
        player.input_enabled = False
        menu_overlay.enabled = True
        respawn_text.enabled = True
    
    #Continuiesly runs when you are dead
    if player.dead and not 5 < abs(time.perf_counter()-player.death_timer):
        print("still dead")
        timer = "Respawning in " + str(round(5 - time.perf_counter() + player.death_timer, 1))
        respawn_text.text = timer
        respawn_text.enabled = True
        player_shadow.enabled = False
    #Runs once when you respawn
    elif player.dead:
        player.dead = False
        print("alive")
        player.input_enabled = True
        player.enabled = True
        respawn_text.enabled = False
        menu_overlay.enabled = False
        cam_switching()
        player.position = (0.5, 1.0,0.5)


    #use this for taking a overview screenshot
    '''
    camera.position = (0, 100, 0)
    camera.rotation = (90, 0, 0) 
    '''
app.run()
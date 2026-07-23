from typing import TYPE_CHECKING
from random import randint

if TYPE_CHECKING:
    from scripts.game.player import _Player
from ursina import *
from scripts.game.controls import *
from scripts.game.settings import MAX_CAM_COST, FASTER_RELOAD_COST
from scripts.game.settings import DEFAULT_NAMES


class UIController:
    def __init__(self, player, mouse):
        self.player:"_Player" = player
        self.mouse = mouse
        self.menu_overlay = Entity(scale = (2,2) , parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)
        self.control_button_list = []
        self.control_buttons_dict = {}
        self.respawn_text = Text("test", origin = (0,0),position = (0,0,-2),
                                  scale = 3, color=color.red,enabled = False)
        self.text_box = Entity(scale = (0.4,0.1) ,origin = (0,0), position = (-.6,-.4),
                                    parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), enabled = True)
        self.cooldown_text = Text("test", origin = (0,0),position = (-.6,-.4,-.9),
                                   scale = 1.5, color=color.green,enabled = True)
        self.camoverlay = Text (parent = camera.ui,scale=2,position=(-0.7,0.4),
                                    color=color.gray, enabled = False)
        self.chat_overlay = Entity(scale = (0.55,0.25) , parent = camera.ui, model = 'quad',
                                    color = color.rgba(0,0,0,0.6), z = -1, enabled = False, position = (0.95,-.275,-1), origin = (0.8,0))

        self.leaderboard_text = Text(f"{self.player.points} {self.player.username} \n round wins: {self.player.round_wins}",
                                      origin = (0,0), position = (0,0), scale = 1.1, color=color.white, enabled= False, z = -2)
        self.leaderboard_overlay = Entity(scale = (0.5,1) , parent = camera.ui,
                                           model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)
        
        self.round_timer_text = Text("", position = (0,0.3), scale = 2, enabled = False, origin = (0,0))
        self.shop_timer_text = Text("", position = (0,0.2), scale = 0.5, enabled = False, origin = (0,0))

        #Main menu
        self.background = Entity(model="quad", texture="hair", scale = (2,2), enabled = False, parent=camera.ui, z = -3)
        self.open_game_button = Button(model = "quad", scale = 0.2, position =(0,0, -4),
                                        color=color.white, text = "Open Game", text_color=color.black)
        self.host_game_button = Button(model = "quad", scale = 0.2, position =(0.25,0, -4),
                                        color=color.white, text = "Host game", text_color=color.black)
        self.map_selector_button = Button(model = "quad", scale = 0.2, position = (-0.25, 0, -4),
                                           color=color.white, text = "map selector", text_color=color.black) 
        self.join_friend_button = Button(model = "quad", scale = (0.6,0.1), position = (0,-0.25, -4),
                                          color=color.white, text = "Join Friend", text_color=color.black)
        self.name_input = InputField(default_value= "Username Here",character_limit = 15, position=(0, -0.15),
                                      scale=(0.3, 0.05), z = -5, color = color.white, enabled = False, text_color=color.black)
        self.exit_game_button = Button(model = "quad", scale = (0.6,0.075), position = (0,-0.4, -4),
                                          color=color.white, text = "Exit game", text_color=color.black)
        self.lobby_botton = Button(model = "quad", scale = (0.2), position = (-1.778*.5,-0.5, -4), origin=(-.5, -.5),
                                          color=color.white, text = "Lobby", text_color=color.black)
        self.name_input.highlight_color = color.white
        self.name_input.highlight_text_color = color.black
        self.name_input.text_color = color.black

        #Join friend:
        self.join_game_button = Button(model = "quad", scale = (0.6,0.1), position = (0,-0.25, -4),
                                        color=color.white, text = "Join Game", text_color=color.black, enabled = False)
        self.host_input = InputField(default_value= "0.0.0.0", position=(0, 0.15), scale=(0.5, 0.05), z = -5,
                                      color = color.white, enabled = False, text_color=color.black)
        self.host_input.highlight_color = color.white  
        self.host_input.highlight_text_color = color.black
        self.host_input.text_color = color.black

        self.port_input = InputField(default_value = "1983", position=(0, 0), scale=(0.5, 0.05), z = -5,
                                      color = color.white, enabled = False, text_color=color.black, limit_content_to='0123456789')
        self.port_input.highlight_color = color.white  
        self.port_input.highlight_text_color = color.black
        self.port_input.text_color = color.black
        self.port_text = Text(text = "port", position=(0, -0.05), origin = (0, 0), text_size = 0.4 , z = -5, color = color.white, enabled = False)
        self.hostname_text = Text(text = "hostname", position=(0, .10), origin = (0, 0), text_size = 0.4 , z = -5, color = color.white, enabled = False)

        #Host game
        self.server_text = Text(position = (0, .1, -4), origin = (0, 0), enabled = False, color=color.black)
        self.start_server_button = Button(model = "quad", scale = (0.6,0.1), position = (0,-0.25, -4),
                                        color=color.white, text = "Start server", text_color=color.black, enabled = False)
        self.has_window_checkbox = Checkbox(start_value=False, scale = (0.1), position = (.35, 0, -4),
                                            enabled = False)
        self.auto_join_checkbox = Checkbox(start_value=False, scale = (0.1), position = (-.35, 0, -4),
                                            enabled = False)
        self.auto_join_text = Text(text="Auto join server", origin = (0, 0), position = (-.35, -.1, -4), enabled = False)
        self.has_window_text = Text(text="Start with window", origin = (0, 0), position = (.35, -.1, -4), enabled = False)


        #Map selector
        self.map_selector_text = Text("Maps", origin = (0,0),position = (0,0.4,-4), scale = 3,
                                       color=color.red, enabled = False)
        self.back_to_main_button = Button(model = "quad", scale = 0.2, position = (-0.8,-0.4,-4),
                                          text = "Back to \n main menu", color=color.orange, enabled = False)

        #Lobby
        self.lobby_text = Text(text = "Connected_Users:", origin = (0, 0.5), position = (0, .5, -4), enabled = False)
        self.start_game_button = Button (model = "quad", scale = (0.6,0.075), position = (0, -.5, -4), origin=(0, -.5),
                                          color=color.white, text = "Start game", text_color=color.black, enabled = False)

        #Buttons Inside the shop
        self.upgrade_cams_button = Button(model = "quad", scale = 0.2, x = -0.1, z = -2,
                                            color=color.gray,
                                            text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${MAX_CAM_COST[0]}" ,
                                            text_size = 0.8, text_color = color.black, enabled = False)
        self.faster_reload_button = Button(model = "quad", scale = 0.2, x = 0.1, z = -2,
                                            color=color.gray,
                                            text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${FASTER_RELOAD_COST[0]}",
                                            text_size = 0.8, text_color = color.black, enabled = False)
        self.shop_buttons_list = [self.upgrade_cams_button,self.faster_reload_button]
        
        #Cash shown inside the shop
        self.current_cash = Text(f"{player.cash} cash", origin = (0,0), position = (-.7,.4,-2), scale = 1, enabled = False)
        
        #Chat message
        self.chat_field = InputField(position = (0.4, -0.45), scale = (0.65,0.03),
                                      color = color.white, enabled = False, text_color = color.black, character_limit = 32)
        self.chat_field.highlight_color = color.white  
        self.chat_field.highlight_text_color = color.black
        self.chat_field.text_color = color.black
        
        #Buy phase
        self.buy_text = Text("BUY PHASE",position = (0,0.3), scale = 2, enabled = False, origin = (0,0))
        self.buy_overlay = Entity(scale = (0.3,0.15), parent = camera.ui, origin = (0,0), position = (0,0.3), model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)


        #Volume sliders
        self.gun_volume_slider = ThinSlider(text='Gun Volume', dynamic=True,
                               max = 100, step = 1, default = 50,
                               position = (-.25, 0, -2),
                               enabled = False)
        self.gun_volume_slider.label.origin = (0,0)
        self.gun_volume_slider.label.position = (.25, -.05)

        self.player_volume_slider = ThinSlider(text='Footstep Volume',dynamic=True,
                                    max = 100, step = 1, default = 50,
                                    position = (-.25, -.2, -2),
                                    enabled = False)
        self.player_volume_slider.label.origin = (0,0)
        self.player_volume_slider.label.position = (.25, -0.06)

        #Control menu buttons
        self.create_control_buttons()
        self.reset_controls_to_default_button = Button(model = "quad", color=color.gray,
                                                        scale = 0.2,  position = (-.8, .4, -2),
                                                        text = "Reset Keybinds", text_size = 0.8, text_color = color.black,
                                                        enabled = False)
        self.control_button_list.append(self.reset_controls_to_default_button)

        #Win / lose result screen text
        self.win_text = Text(f'{self.player.username} WINS!!!', origin = (0,0), position = (0,0,-1.1),
                              scale = 5, color=color.green,enabled = False)
        self.lose_text = Text(f'{self.player.username} WINS!!!', origin = (0,0), position = (0,0,-1.1),
                               scale = 5, color=color.red,enabled = False)
        self.draw_text = Text('DRAW!!!', origin = (0,0),position = (0,0,0), scale = 5, color=color.gray,enabled = False)

        #Escape menu buttons
        self.quit_button = Button(model = "quad", scale = 0.2, x = 0, y=-.2, z = -2, color=color.gray,
                                   text = "Quit Game", text_size = 0.8, text_color = color.black, enabled = False)
        self.volume_button = Button(model = "quad", scale = 0.2, x = 0.2, z = -2, color = color.gray,
                                     text = "volume controls", text_size = 0.8, text_color = color.black, enabled = False)
        self.control_button = Button(model = "quad", scale = 0.2, x = -0.2, z = -2, color = color.gray,
                                      text = "controls", text_size = 0.8, text_color = color.black, enabled = False)
        self.resume_button = Button(model = "quad", scale = 0.2, z = -2, color=color.gray, text = "Resume",
                                     text_size = 0.8, text_color = color.black, enabled = False)
        self.button_list = [self.volume_button,self.quit_button,self.control_button,self.resume_button]

    def control_changer(self,control,button) -> None:
        self.player.control_change_button_pressed = True
        self.player.control_change_key = control
        button.text = "Press a key to assign\n it to this action"

        #Creates the buttons and adds them to a list and dictionary
    def create_control_buttons(self) -> None:
        for name, control, x, y in control_button_data_list:
            button = Button(model = "quad",
                            scale = 0.2, x = x, y = y,z = -2,color = color.gray,
                              text = f"{name} \n{get_binding(control)}",
                            text_size =0.8, text_color= color.black, enabled = False)
            button.name = name
            button.on_click = Func(self.control_changer, control,button)
            self.control_button_list.append(button)
            self.control_buttons_dict[control] = button


    def ui_changer(self, is_open = False) -> None:
        for button in self.button_list:
            button.enabled = is_open
        for upgrades in self.shop_buttons_list:
            upgrades.enabled = False

    def open_shop_menu(self, is_open = False) -> None:
        self.menu_overlay.enabled = is_open
        self.upgrade_cams_button.enabled = is_open
        self.faster_reload_button.enabled = is_open
        self.mouse.visible = is_open
        self.mouse.locked = not is_open
        self.player.cursor.enabled = not is_open
        self.current_cash.enabled = is_open

    def open_volume_menu(self, is_open = True) -> None:
        self.ui_changer()
        self.menu_overlay.enabled = is_open
        self.gun_volume_slider.enabled = is_open
        self.player_volume_slider.enabled = is_open

    def open_control_menu(self, is_open = True) -> None:
        self.ui_changer()
        self.menu_overlay.enabled = is_open
        for button in self.control_button_list:
            button.enabled = is_open

    def update_control_text(self) -> None:
        '''Update the control buttons text after it changes'''
        for control, button in self.control_buttons_dict.items():
            button.text = f'{button.name}\n{get_binding(control)}'
        #Function used to reset controls

    def set_mouse_menu_state(self) -> None:
        '''Sets the mouse to the menu state'''
        self.mouse.visible = True
        self.mouse.locked = False
        self.player.cursor.enabled = False

    def set_mouse_game_state(self):
        '''Sets the mouse to the game state'''
        self.mouse.visible = False
        self.mouse.locked = True
        self.player.cursor.enabled = True

    def toggle_leaderboard(self, enabled) -> None:
        '''If true: shows leaderboard, if false: hides leaderboard'''
        self.leaderboard_text.enabled = enabled
        self.leaderboard_overlay.enabled = enabled

    def reset_input_field(self, input_field:InputField):
        if input_field.text == input_field.default_value:
            input_field.text = ""

    def reset_and_update_controls(self) -> None:
        reset_controls_to_default()
        self.update_control_text()

    def close_all_uis(self) -> None:
        self.open_control_menu(False)
        self.open_shop_menu(False)
        self.open_volume_menu(False)
        self.set_mouse_game_state()
        self.player.in_menu = False

    def acquire_and_set_name(self) -> str:
        '''Gets the player name from the input, sets it to the username, and returns it'''
        if not self.name_input.text.strip() or self.name_input.text == self.name_input.default_value:
            self.player.username = DEFAULT_NAMES[randint(0,29)]
        else:
            self.player.username = self.name_input.text
        return self.player.username

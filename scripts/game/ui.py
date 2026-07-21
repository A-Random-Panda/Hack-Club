from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.game.player import _Player
from ursina import *
from scripts.game.controls import *
from scripts.game.settings import MAX_CAM_COST, FASTER_RELOAD_COST



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

        self.leaderboard_text = Text(f"{self.player.points} {self.player.username}",
                                      origin = (0,0), position = (0,0), scale = 1.1, color=color.white, enabled= False, z = -2)
        self.leaderboard_overlay = Entity(scale = (0.5,1) , parent = camera.ui,
                                           model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)
        
        #Main menu
        self.background = Entity(model="quad", scale = (2,2),color = color.black, enabled = False, parent=camera.ui, z = -3)
        self.open_game_button = Button(model = "quad", scale = 0.2, position =(0.2,0, -4),
                                        color=color.white, text = "Host game", text_color=color.black)
        self.map_selector_button = Button(model = "quad", scale = 0.2, position = (-0.2, 0, -4),
                                           color=color.white, text = "map selector", text_color=color.black) 
        self.join_friend_button = Button(model = "quad", scale = (0.6,0.1), position = (0,-0.25, -4),
                                          color=color.white, text = "Join Friend", text_color=color.black)
        self.name_input = InputField(default_value= "Username Here",character_limit = 15, position=(0, -0.15),
                                      scale=(0.3, 0.05), z = -5, color = color.white, enabled = False, text_color=color.black)
        self.name_input.highlight_color = color.white  
        self.name_input.highlight_text_color = color.black
        self.name_input.text_color = color.black

        #Join friend:
        self.join_game_button = Button(model = "quad", scale = (0.6,0.1), position = (0,-0.25, -4),
                                        color=color.white, text = "Join Game", text_color=color.black, enabled = False)
        self.host_input = InputField(default_value= "localhost", position=(0, 0.15), scale=(0.5, 0.05), z = -5,
                                      color = color.white, enabled = False, text_color=color.black)
        self.host_input.highlight_color = color.white  
        self.host_input.highlight_text_color = color.black
        self.host_input.text_color = color.black

        self.port_input = InputField(default_value = "1983", position=(0, 0), scale=(0.5, 0.05), z = -5,
                                      color = color.white, enabled = False, text_color=color.black, limit_content_to='0123456789')
        self.port_input.highlight_color = color.white  
        self.port_input.highlight_text_color = color.black
        self.port_input.text_color = color.black
        self.port_text = Text(text = "port value", position=(-0.08, -0.05), text_size = 0.4 , z = -5, color = color.white, enabled = False)

        #Map selector
        self.map_selector_text = Text("Maps", origin = (0,0),position = (0,0.4,-4), scale = 3,
                                       color=color.red,enabled = False)
        self.back_to_main_button = Button(model = "quad", scale = 0.2, position = (-0.8,-0.4,-4),
                                          text = "Back to \n main menu", color=color.orange, enabled = False)

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
        
        #Volume sliders
        self.gun_volume_slider = ThinSlider(text='Gun Volume',
                               dynamic=True,
                               max = 100,
                               step = 1,
                               z = -2,
                               x = -.25,
                               y = 0,
                               enabled = False,
                               default = 50,
                               )
        self.gun_volume_slider.label.origin = (0,0)
        self.gun_volume_slider.label.position = (.25, -.05)

        self.player_volume_slider = ThinSlider(text='Footstep Volume',
                                    dynamic=True,
                                    max = 100,
                                    z = -2,
                                    step = 1,
                                    x =-.25,
                                    y=-.2,
                                    enabled = False,
                                    default = 50,
                                    )
        self.player_volume_slider.label.origin = (0,0)
        self.player_volume_slider.label.position = (.25, -0.06)

        #Control menu buttons
        self.create_control_buttons()
        self.reset_controls_to_default_button = Button(model = "quad",
                                                        scale = 0.2,
                                                        x = -0.8,
                                                        y = 0.4,
                                                        z = -2,
                                                        color=color.gray,
                                                        text = "Reset Keybinds",
                                                        text_size = 0.8,
                                                        text_color = color.black,
                                                        enabled = False)
        self.control_button_list.append(self.reset_controls_to_default_button)

        #Win / lose result screen text
        self.win_text = Text(f'{self.player.username} WINS!!!', origin = (0,0), position = (0,0,-1.1),
                              scale = 5, color=color.green,enabled = False)
        self.lose_text = Text(f'{self.player.username} WINS!!!', origin = (0,0),position = (0,0,-1.1),
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


    def ui_changer(self, boolean = False) -> None:
        for button in self.button_list:
            button.enabled = boolean
        for upgrades in self.shop_buttons_list:
            upgrades.enabled = False

    def open_shop_menu(self, boolean = False) -> None:
        self.menu_overlay.enabled = boolean
        self.upgrade_cams_button.enabled = boolean
        self.faster_reload_button.enabled = boolean
        self.mouse.visible = boolean
        self.mouse.locked = not boolean
        self.player.cursor.enabled = not boolean
        self.current_cash.enabled = boolean

    def open_volume_menu(self, boolean = True) -> None:
        self.ui_changer()
        self.menu_overlay.enabled = boolean
        self.gun_volume_slider.enabled = boolean
        self.player_volume_slider.enabled = boolean

    def open_control_menu(self, boolean = True) -> None:
        self.ui_changer()
        self.menu_overlay.enabled = boolean
        for button in self.control_button_list:
            button.enabled = boolean
    #Update the control buttons text after it changes
    def update_control_text(self) -> None:
        for control, button in self.control_buttons_dict.items():
            button.text = f'{button.name}\n{get_binding(control)}'
        #Function used to reset controls

    def mouse_in_menu(self, boolean = True) -> None:
        self.mouse.visible = boolean
        self.mouse.locked = not boolean
        self.player.cursor.enabled = not boolean

    def open_leaderboard(self, boolean) -> None:
        self.leaderboard_text.enabled = boolean
        self.leaderboard_overlay.enabled = boolean

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
        self.mouse_in_menu(False)
        self.player.in_menu = False

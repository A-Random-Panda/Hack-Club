from ursina import *
from scripts.controls import *
from scripts.settings import MAX_CAM_COST, FASTER_RELOAD_COST



class UIController:
    def __init__(self, player, mouse):
        self.player = player
        self.mouse = mouse
        self.menu_overlay = Entity(scale = (2,2) , parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), z = -1, enabled = False)
        self.control_button_list = []
        self.control_buttons_dict = {}
        self.create_control_buttons()
        self.respawn_text = Text("test", origin = (0,0),position = (0,0,-2), scale = 3, color=color.red,enabled = False)
        self.text_box = Entity(scale = (0.4,0.1) ,origin = (0,0), position = (-.6,-.4), parent = camera.ui, model = 'quad', color = color.rgba(0,0,0,0.6), enabled = True)
        self.cooldown_text = Text("test", origin = (0,0),position = (-.6,-.4,-.9), scale = 1.5, color=color.green,enabled = True)
        self.camoverlay = Text (parent = camera.ui,scale=2,position=(-0.7,0.4),color=color.gray, enabled = False)



        #Buttons Inside the shop
        self.upgrade_cams_button = Button(model = "quad", scale = 0.2, x = -0.1, z = -2, color=color.gray, text = f"+1 Max cam \n current cams: {player.max_cams} \n cost: ${MAX_CAM_COST[0]}" , text_size = 0.8, text_color = color.black, enabled = False)
        #self.upgrade_cams_button.on_click = cam_upgrade -> move to main
        self.faster_reload_button = Button(model = "quad", scale = 0.2, x = 0.1, z = -2, color=color.gray, text = f"-0.5 sec reload time \n reload time: {player.reload_time} sec \n cost: ${FASTER_RELOAD_COST[0]}", text_size = 0.8, text_color = color.black, enabled = False)
        #self.faster_reload_button.on_click = reload_upgrade -> move to main
        self.shop_buttons_list = [self.upgrade_cams_button,self.faster_reload_button]
        #Cash shown inside the shop
        self.current_cash = Text(f"{player.cash} cash", origin = (0,0), position = (-.7,.4,-2), scale = 1, enabled = False)
        
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

        self.reset_controls_to_default_button = Button(model = "quad", scale = 0.2, x = -0.8, y = 0.4,z = -2,color=color.gray,
                                        text = "Reset Keybinds", text_size = 0.8, text_color = color.black, enabled = False)
        self.control_button_list.append(self.reset_controls_to_default_button)



        #Main menu escape buttons
        self.quit_button = Button(model = "quad", scale = 0.2, x = 0, z = -2, color=color.gray, text = "Quit Game", text_size = 0.8, text_color = color.black, enabled = False)
        #quit_button.on_click = application.quit
        self.volume_button = Button(model = "quad", scale = 0.2, x = 0.2, z = -2, color = color.gray, text = "volume controls", text_size = 0.8, text_color = color.black, enabled = False)
        #self.volume_button.on_click = self.open_volume_menu
        self.control_button = Button(model = "quad", scale = 0.2, x = -0.2, z = -2, color = color.gray, text = "controls", text_size = 0.8, text_color = color.black, enabled = False)
        #self.control_button.on_click = self.open_control_menu
        self.button_list = [self.volume_button,self.quit_button,self.control_button]
        

    def control_changer(self,control,button):
        self.player.control_change_button_pressed = True
        self.player.control_change_key = control
        button.text = "Press a key to assign\n it to this action"

        #Creates the buttons and adds them to a list and dictionary
    def create_control_buttons(self):
        for name, control, x, y in control_button_data_list:
            button = Button(model = "quad",
                            scale = 0.2, x = x, y = y,z = -2,color = color.gray, text = f"{name} \n{get_binding(control)}",
                            text_size =0.8, text_color= color.black, enabled = False)
            button.name = name
            button.on_click = Func(self.control_changer, control,button)
            self.control_button_list.append(button)
            self.control_buttons_dict[control] = button


    def ui_changer(self,boolean = False):
        for button in self.button_list:
            button.enabled = boolean
        for upgrades in self.shop_buttons_list:
            upgrades.enabled = False

    def open_shop_menu(self, boolean = False):
        self.menu_overlay.enabled = boolean
        self.upgrade_cams_button.enabled = boolean
        self.faster_reload_button.enabled = boolean
        self.mouse.visible = boolean
        self.mouse.locked = not boolean
        self.player.cursor.enabled = not boolean
        self.current_cash.enabled = boolean

    def open_volume_menu(self,boolean = True):
        self.ui_changer()
        self.menu_overlay.enabled = boolean
        self.gun_volume_slider.enabled = boolean
        self.player_volume_slider.enabled = boolean

    def open_control_menu(self,boolean = True):
        self.ui_changer()
        self.menu_overlay.enabled = boolean
        for button in self.control_button_list:
            button.enabled = boolean
    #Update the control buttons text after it changes
    def update_control_text(self):
        for control, button in self.control_buttons_dict.items():
            button.text = f'{button.name}\n{get_binding(control)}'
        #Function used to reset controls
    def reset_and_update_controls(self):
        reset_controls_to_default()
        self.update_control_text()
'''This module contains the player class for the game'''
from typing import Any, override
from ursina import *
from scripts.helper.editable_controls_FPC import FirstPersonController
from scripts.game.controls import *


_player_properties:dict[str,Any] = {
        "collider": "box",
        "position":(0.5,1,0.5),
        "speed":8,
        "jump_height":4,
        "gravity":1
        }

class _Player(FirstPersonController):
    '''The player class for the game'''
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) #pylint: disable=no-value-for-parameter
        return cls._instance
    def __init__(self):
        super().__init__(**_player_properties)
        self.in_camera:bool = False
        self.current_cam:int = 0
        self.perspective_list:list[Entity] = []
        self.cam_icon_list:list[Entity] = []
        self.cd:float = 0.0
        self.bullet_trail:Entity|None = None
        self.in_menu:bool = False
        self.changed_key:str|None = None
        self.control_change_button_pressed:bool =  False
        self.control_change_key = None
        self.max_cams:int = 5
        self.cash:int = 100000
        self.reload_time:float = 5.0
        self.in_shop:bool = False
        self.dead:bool = False
        self.death_timer:float = 0.0
        self.input_enabled:bool = True
        self.in_zone:bool = False
        self.points:int = 0
        self.in_main_menu:bool = False
        self.username:str = ""
        self.in_chat:bool = False
        self.chat_opened:float = 0.0
        self.message:Entity = None
        self.laser:Entity = None
        self.respawn_point:Vec3 = (0,2,0)
        self.rounds:int = 0
        self.lose_streak: int = 0
        self.in_buy_phase: bool  = False
        self.in_round: bool = False
        self.round_timer: float = 0.0


    @override
    def update(self):
        if self.in_main_menu:
            return
        elif self.in_chat:
            super().update()
        else:
            super().update()
            if self.in_menu or self.in_shop: 
                super().movement()

            
            elif self.in_camera:
                cam = self.perspective_list[self.current_cam]
                cam.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
                cam.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
                cam.camera_pivot.rotation_x= clamp(cam.camera_pivot.rotation_x, -20, 10)
                cam.rotation_y= clamp(cam.rotation_y, cam.original_rotation_y-40, cam.original_rotation_y+40)
                super().movement()
            
            else:
                super().movement()
                super().mouse_movement()
    def input(self, key):
        if self.in_chat:
            return

        if key == get_binding(Controls.JUMP):
            self.jump()
            

def get_player() -> _Player:
    '''
    Returns the player object.
    This is unnecessary because the player is a singleton, but it exists for legacy reasons
    '''
    return _Player()
if __name__ == "__main__":
    print(_Player() == _Player())



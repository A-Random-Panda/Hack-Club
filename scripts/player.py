'''This module contains the player class for the game'''
from typing import Any
from ursina import *
from scripts.editable_controls_FPC import FirstPersonController


_player_properties:dict[str,Any] = {
        "collider": "box",
        "position":(0.5,1,0.5),
        "speed":8,
        "jump_height":4,
        "gravity":1
        }

class _Player(FirstPersonController):
    '''The player class for the game'''
    def __init__(self):
        super().__init__(**_player_properties)
        self.in_camera:bool = False
        self.current_cam:int = 0
        self.perspective_list:list[Entity] = []
        self.cam_icon_list:list[Entity] = []
        self.cd:float = 0.0
        self.bullet_trail = None #entity
        self.in_menu:bool = False
        self.changed_key = None #str
        self.control_change_button_pressed:bool =  False
        self.control_change_key = None
        self.max_cams:int = 5
        self.cash:int = 100000
        self.reload_time:float = 5.0
        self.in_shop:bool = False
        self.dead:bool = False
        self.death_timer:float = 0.0
        self.input_enabled:bool = True
    def update(self):
        super().update()
        if self.in_camera and not self.in_menu:
            cam = self.perspective_list[self.current_cam]
            cam.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
            cam.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
            cam.camera_pivot.rotation_x= clamp(cam.camera_pivot.rotation_x, -20, 10)
            cam.rotation_y= clamp(cam.rotation_y, cam.original_rotation_y-40, cam.original_rotation_y+40)
            #
            super().movement_in_cam()
        elif self.in_menu or self.in_shop: 
            super().movement_not_in_cam()
        else:
            super().movement_not_in_cam()
            super().mouse_movement_not_in_cam()
            

#This is probably not the best way to make a singleton esque thing, but it works okay?
_player_list:list[_Player] = []
def get_player() -> _Player:
    '''Returns the player object'''
    if len(_player_list) > 1:
        pass
    else:
        _player_list.append(_Player())
    return _player_list[0]

if __name__ == "__main__":
    pass

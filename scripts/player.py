'''This module contains the player class for the game'''
from typing import Any
from scripts.editable_controls_FPC import FirstPersonController

_player_properties:dict[str,Any] = {
        "collider":"box",
        "position":(0.5,1,0.5),
        "speed":20,
        "jump_height":4,
        "gravity":1
        }

class _Player(FirstPersonController):
    '''The player class for the game'''
    def __init__(self):
        super().__init__(**_player_properties)
        self.in_camera:bool = False
        self.current_cam:int = 0
        self.perspective_list:list[object] = []
        self.camera_entity_list:list[object] = []

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

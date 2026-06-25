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
    in_camera:bool = False
    current_cam:int = 0
    saved_pos:tuple[float, float, float] = (0, 0, 0)
    saved_rot:tuple[float, float, float] = (0, 0, 0)
    perspective_list:list[object] = []
    
    def __init__(self):
        super().__init__(kwargs=_player_properties)

player = _Player()

if __name__ == "__main__":
    pass

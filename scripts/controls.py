'''This file contains the default controls, and obtains the controls from controls.json
TODO: Implement the JSON to controls part
'''

class _Controls():
    #default controls
    CONTROL_LIST:list[str] = []
    MOVE_FORWARDS:str = 'w'
    MOVE_BACKWARDS:str = 's'
    MOVE_LEFT:str = 'a'
    MOVE_RIGHT:str = 'd'
    JUMP:str = 'space'
    TOGGLE_CAMERA:str = 'c'
    RESET_CAMERAS:str = 'r'
    PLACE_CAMERA:str = 'left mouse down'
    FREECAM_MODE:str = 'p'
    QUIT_GAME:str = 'escape'
    _CONTROL_MAP:dict[str,object] = {
                "Move Forwards":MOVE_FORWARDS,
                "Move Backwards":MOVE_BACKWARDS,
                "Move Left":MOVE_LEFT,
                "Move Right":MOVE_RIGHT,
                "Jump":JUMP,
                "Toggle Camera":TOGGLE_CAMERA,
                "Reset Camera":RESET_CAMERAS,
                "Place Camera":PLACE_CAMERA,
                "Freecam":FREECAM_MODE,
                "Quit:":QUIT_GAME
    }
    def __init__(self) -> None:
        self.CONTROL_LIST = list(self._CONTROL_MAP.keys())

    def _change_controls(self, changed_controls:dict) -> None:
        for k,v in changed_controls:
            if k in self._CONTROL_MAP.keys():
                self._CONTROL_MAP[k] = v

CONTROLS:_Controls = _Controls()


if __name__ == "__main__":
    #For testing
    print(f"Controls are set to {CONTROLS._CONTROL_MAP}.")
    print(f"Controls are {CONTROLS.CONTROL_LIST}")
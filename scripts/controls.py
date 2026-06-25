'''
This file contains the controls for the game
It contains default controls, and also the ability to modify the control to ones in controls.json
'''

from pathlib import Path as _Path
import json as _json
import logging as _logging

_logger:_logging.Logger = _logging.getLogger(__name__)

#Default controls
#To add more controls, create a new variable, set it equal to the default control
#And add it to dictionary with control_name:control_variable
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
CONTROL_LIST:tuple[str, ...] = tuple(_CONTROL_MAP.keys())

def _change_controls(changed_controls:dict) -> None:
    '''Changes controls to be the one in the dictionary'''
    for k,v in changed_controls:
        if k in _CONTROL_MAP:
            _CONTROL_MAP[k] = v
        else:
            _logger.warning("Found non-existant control %s.", k)

def _get_json_path() -> _Path:
    '''Returns the path of the controls.json file'''
    script_path = str(_Path(__file__).resolve().parent)
    last_slash_index = script_path.rfind("\\")
    return _Path(script_path[0:last_slash_index+1] + "controls.json")

def set_controls() -> None:
    '''Changes controls to the controls found in the controls.JSON file'''

    #Ensures there is a control file
    if not _get_json_path().is_file():
        _Path(_get_json_path()).touch()
        _logger.info("Creating file %s", _get_json_path)

    #Reads the changes
    with open(_get_json_path(), "r", encoding="utf-8") as json_file:
        _control_changes = json_file.read()

    #Ensures file is not empty
    if _control_changes.isspace() or len(_control_changes) == 0:
        return

    #Sets changes
    try:
        _control_changes = _json.loads(_control_changes)
        if not _control_changes.isinstance(dict):
            _logger.error("Controls file didn't return a dictionary")
            _logger.info("Falling back to default controls.")
        else:
            _change_controls(_control_changes)
    except _json.JSONDecodeError:
        _logger.error("Controls file is not formatted as a json.")
        _logger.info("Falling back to default controls.")

set_controls()

if __name__ == "__main__":
    #For testing
    print(f"Controls are set to {_CONTROL_MAP}.")
    print(f"Controls are {CONTROL_LIST}")
    print(_get_json_path())

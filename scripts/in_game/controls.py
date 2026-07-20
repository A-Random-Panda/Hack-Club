'''
This file contains the controls for the game
It contains default controls, and also the ability to modify the control to ones in controls.json
'''

from pathlib import Path as _Path
from enum import IntEnum as _IntEnum
from copy import deepcopy
import json as _json
import logging as _logging

_logger:_logging.Logger = _logging.getLogger(__name__)

#Default controls
#To add more controls, create a new variable in the enum 
#And add it to _BINDINGS_DICT with control:default_value
#Also add it to _CONTROL_NAMES

class Controls(_IntEnum):
    '''Enum containing the controls for the game'''
    MOVE_FORWARDS = 0
    MOVE_BACKWARDS = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    JUMP = 4
    TOGGLE_CAMERA = 5
    RESET_CAMERAS = 6
    PLACE_CAMERA = 7
    FREECAM_MODE = 8
    QUIT_GAME = 9
    CAMERA_LEFT = 10
    CAMERA_RIGHT = 11
    SHOOT = 12
    OPEN_SHOP = 13
    CHECK_LEADERBOARD = 14
    OPEN_CHAT = 15
    SEND_MSG = 16

_UNCHANGABLE_CONTROLS = [
    Controls.QUIT_GAME
]

_BINDINGS_DICT:dict[Controls, str] = {
    Controls.MOVE_FORWARDS:"w",
    Controls.MOVE_BACKWARDS:"s",
    Controls.MOVE_LEFT:"a",
    Controls.MOVE_RIGHT:"d",
    Controls.JUMP:"space",
    Controls.TOGGLE_CAMERA:"c",
    Controls.RESET_CAMERAS:"r",
    Controls.PLACE_CAMERA:"left mouse down",
    Controls.FREECAM_MODE:"p",
    Controls.QUIT_GAME:"escape",
    Controls.CAMERA_LEFT: "left arrow",
    Controls.CAMERA_RIGHT: "right arrow",
    Controls.SHOOT: "f",
    Controls.OPEN_SHOP: "b",
    Controls.CHECK_LEADERBOARD: "tab",
    Controls.OPEN_CHAT: "y",
    Controls.SEND_MSG: "enter"
}

_CONTROL_NAMES:dict[str, Controls] = {
    "Move Forwards" : Controls.MOVE_FORWARDS,
    "Move Backwards" : Controls.MOVE_BACKWARDS,
    "Move Left" : Controls.MOVE_LEFT,
    "Move Right" : Controls.MOVE_RIGHT,
    "Jump" : Controls.JUMP,
    "Toggle Camera" : Controls.TOGGLE_CAMERA,
    "Reset Cameras" : Controls.RESET_CAMERAS,
    "Place Camera" : Controls.PLACE_CAMERA,
    "Freecam" : Controls.FREECAM_MODE,
    "Quit" : Controls.QUIT_GAME,
    "Pan left" : Controls.CAMERA_LEFT,
    "Pan Right" : Controls.CAMERA_RIGHT,
    "Shoot" : Controls.SHOOT,
    "Open Shop" : Controls.OPEN_SHOP,
    "Check Leaderboard" : Controls.CHECK_LEADERBOARD,
    "Open Chat" : Controls.OPEN_CHAT,
    "Send Message" : Controls.SEND_MSG,
}

_DEFAULT_CONTROLS = deepcopy(_BINDINGS_DICT)

#Control name, enum, x pos, y pos
control_button_data_list = [
    ("Forwards", Controls.MOVE_FORWARDS, 0.4, 0),
    ("Backwards", Controls.MOVE_BACKWARDS, 0.4, 0.2),
    ("Strafe Left", Controls.MOVE_LEFT, 0.4, 0.4),
    ("Strafe Right", Controls.MOVE_RIGHT, 0.4, -0.2),
    ("Jump", Controls.JUMP, 0.4, -0.4),
    ("Open Camera", Controls.TOGGLE_CAMERA, -0.4, 0),
    ("Place Camera", Controls.PLACE_CAMERA, -0.4, -0.2),
    ("Reset All Cameras", Controls.RESET_CAMERAS, -0.4, 0.4),
    ("Shoot", Controls.SHOOT, -0.4, 0.2),
    ("Player Camera Left", Controls.CAMERA_LEFT, -0.4, -0.4),
    ("Player Camera Right", Controls.CAMERA_RIGHT, -0.4, -0.6),
    ("Open Shop", Controls.OPEN_SHOP, 0,0),
    ("Check Leaderboard", Controls.CHECK_LEADERBOARD, 0,-0.2),
    ("Open Chat", Controls.OPEN_CHAT, 0,-0.4),
    ("Send Message", Controls.SEND_MSG, 0, -0.6)
]

def _change_controls(changed_controls:dict) -> None:
    '''Changes controls to be the ones specified in changed_controls dictionary'''
    #Saves automatically as string integers, so this sets them to the integers
    #This is probably bad and hacky, will look at it again later
    for k in list(changed_controls.keys()):
        #Checks if k is a string, then, if so, if it's an integer
        if isinstance(k, str):
            if k.isdigit():
                changed_controls[int(k)] = changed_controls.pop(k)
    _logger.debug("Control: %s", changed_controls)
    #Iterates over dict
    for k,v in changed_controls.items():
        #Check the control actually exists
        if k not in _BINDINGS_DICT:
            _logger.warning("Found non-existant control %s.", k)
        else:
            #If the control is unchangable and not the default value
            if k in _UNCHANGABLE_CONTROLS and _BINDINGS_DICT[k] != v:
                _logger.warning("Unchangable control %s attempted to be changed.", k)
            else:
                _BINDINGS_DICT[k] = v       

def _get_json_path() -> _Path:
    '''Returns the path of the controls.json file'''
    script_path = str(_Path(__file__).resolve().parent)
    last_slash_index = script_path.rfind("\\")
    return _Path(script_path[0:last_slash_index+1] + "controls.json")

def _load_controls() -> None:
    '''Changes controls to the controls found in the controls.JSON file'''

    _control_changes_dict:dict[int, str] = {}

    #Ensures there is a control file
    if not _get_json_path().is_file():
        reset_controls_to_default()
        _logger.info("Creating file %s", _get_json_path)

    #Reads the changes
    with open(_get_json_path(), "r", encoding="utf-8") as json_file:
        _control_changes:str = json_file.read()

    #Ensures file is not empty
    if _control_changes.isspace() or len(_control_changes) == 0:
        return

    #Sets changes
    try:
        _control_changes_dict = _json.loads(_control_changes)
        if not isinstance(_control_changes_dict, dict):
            _logger.error("Controls file didn't return a dictionary")
            _logger.info("Falling back to default controls.")
        else:
            _logger.debug("Changes imported from json as %s.", _control_changes_dict)
            _change_controls(_control_changes_dict)
    except _json.JSONDecodeError:
        _logger.error("Controls file is not formatted as a json.")
        _logger.info("Falling back to default controls.")

def _save_controls(control_dictionary:dict) -> None:
    '''Save controls to controls.json'''
    with open(_get_json_path(), "w", encoding="utf-8") as json_file:
        _logger.info("Writing dictionary to file.")
        json_file.write(_json.dumps(control_dictionary))

def get_binding(control:Controls) -> str:
    '''Returns the key for a control.'''
    return _BINDINGS_DICT[control]

def set_control(control:Controls, key:str) -> None:
    '''Sets the control to be of value key, and then saves them to controls.json'''
    if control in _UNCHANGABLE_CONTROLS:
        _logger.critical("HARRY YAO IS STUPID AND ALLOWED UNCHANGABLE CONTROLS TO BE CHANGED")
        raise ValueError("HARRY YAO IS STUPID! (unchangable control attempted to be changed)")
    _BINDINGS_DICT[control] = key
    _save_controls(_BINDINGS_DICT)

def reset_controls_to_default() -> None:
    '''Resets controls to their default state.'''
    _BINDINGS_DICT.update(_DEFAULT_CONTROLS)
    _save_controls(_BINDINGS_DICT)

def get_changable_controls() -> dict[str, Controls]:
    '''Returns a dictionary of control name : control'''
    return {k:v for k,v in _CONTROL_NAMES.items() if v not in _UNCHANGABLE_CONTROLS}


_load_controls()

if __name__ == "__main__":
    #For testing
    _logger.info("Controls are set to %s.", _BINDINGS_DICT)
    _save_controls(_BINDINGS_DICT)
    print(get_changable_controls())

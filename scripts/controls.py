'''
This file contains the controls for the game
It contains default controls, and also the ability to modify the control to ones in controls.json
'''

from pathlib import Path as _Path
from enum import Enum as _Enum
import json as _json
import logging as _logging

_logger:_logging.Logger = _logging.getLogger(__name__)

#Default controls
#To add more controls, create a new variable, set it equal to the default control
#And add it to dictionary with control_name:control_variable
class Controls(int, _Enum):
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

UNCHANGABLE_CONTROLS = [
    Controls.QUIT_GAME
]

_BINDINGS_DICT:dict[Controls,str] = {
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
}

def get_binding(control:Controls) -> str:
    '''Gets the binding from a value in the controls enum.'''
    return _BINDINGS_DICT[control]


def _change_controls(changed_controls:dict) -> None:
    '''Changes controls to be the one in the dictionary'''
    #Saves automatically as string integers, so this sets them to the integers
    #This is probably bad and hacky, will look at it again later
    for k in list(changed_controls.keys()):
        if isinstance(k, str):
            if k.isdigit():
                changed_controls[int(k)] = changed_controls.pop(k)
    _logger.debug("Control: %s", changed_controls)
    for k,v in changed_controls.items():
        if k in [x.value for x in _BINDINGS_DICT.keys()] or k in _BINDINGS_DICT:
            if k not in UNCHANGABLE_CONTROLS:
                _BINDINGS_DICT[k] = v
            else:
                _logger.warning("Unchangable control %s attempted to be changed.", k)
        else:
            _logger.warning("Found non-existant control %s.", k)

def _get_json_path() -> _Path:
    '''Returns the path of the controls.json file'''
    script_path = str(_Path(__file__).resolve().parent)
    last_slash_index = script_path.rfind("\\")
    return _Path(script_path[0:last_slash_index+1] + "controls.json")

def _set_controls() -> None:
    '''Changes controls to the controls found in the controls.JSON file'''

    _control_changes_dict:dict[int, str] = {}

    #Ensures there is a control file
    if not _get_json_path().is_file():
        _Path(_get_json_path()).touch()
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

def change_controls(control:Controls, key:"str") -> None:
    '''Changes Control to Key and saves to controls.json'''
    _BINDINGS_DICT[control] = key
    _save_controls(_BINDINGS_DICT)

_set_controls()

if __name__ == "__main__":
    #For testing
    _logger.info("Controls are set to %s.", _BINDINGS_DICT)
    _save_controls(_BINDINGS_DICT)

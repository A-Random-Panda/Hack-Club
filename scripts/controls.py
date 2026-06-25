'''This file contains the default controls, and obtains the controls from controls.json
'''

from pathlib import Path
import json
import logging

logger:logging.Logger = logging.getLogger(__name__)

#default controls
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
            logger.warning("Found non-existant control %s.", k)

def _get_json_path() -> Path:
    '''Returns the path of the controls.json file'''
    script_path = str(Path(__file__).resolve().parent)
    last_slash_index = script_path.rfind("\\")
    return Path(script_path[0:last_slash_index+1] + "controls.json")

def set_controls() -> None:
    '''Changes controls to the controls found in the controls.JSON file'''

    #Ensures there is a control file
    if not _get_json_path().is_file():
        Path(_get_json_path()).touch()
        logger.info("Creating file %s", _get_json_path)

    #Reads the changes
    with open(_get_json_path(), "r", encoding="utf-8") as json_file:
        _control_changes = json_file.read()

    #Ensures file is not empty
    if _control_changes.isspace() or len(_control_changes) == 0:
        return

    #Sets changes
    try:
        _control_changes = json.loads(_control_changes)
        if not _control_changes.isinstance(dict):
            logger.error("Controls file didn't return a dictionary")
            logger.info("Falling back to default controls.")
        else:
            _change_controls(_control_changes)
    except json.JSONDecodeError:
        logger.error("Controls file is not formatted as a json.")
        logger.info("Falling back to default controls.")

set_controls()

if __name__ == "__main__":
    #For testing
    print(f"Controls are set to {_CONTROL_MAP}.")
    print(f"Controls are {CONTROL_LIST}")
    print(_get_json_path())

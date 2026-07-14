'''This contains the map saving sequence for the map maker'''

import json
import logging
from pathlib import Path
from typing import Any

from ursina import *

_logger:logging.Logger = logging.getLogger(__name__)

def _json_dump_map(file_name:str|Path, _map):
    '''Dumps the map to file_name'''
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(json.dumps(_map, default=str))

def save_map(_map:list[Entity]) -> None:
    '''Saves map to file map(number).json'''
    #find path
    save_folder = Path.cwd() / "maps" / "saved maps"
    map_number_file = Path.resolve(save_folder / "nextmapnumber.txt")

    #Check the number file exists
    if not map_number_file.exists():
        _logger.info("Map number file doesn't exist; creating file")
        map_number_file.parent.mkdir(parents=True)
        with open(map_number_file, "w", encoding="utf-8") as file:
            file.write("This file decides the next file, read from the number in the next line\n1")

    #Reads the file
    with open(map_number_file, "r", encoding="utf-8") as file:
        file.readline()
        map_number = file.readline()
    _logger.debug("Next map number read as %s", map_number)

    #Ensures next map is a integer
    if not map_number.isdigit():
        #Fallback if it's not an integer
        _logger.error("Map file is incorrect; map will be saved as errormap.json. Please fix the file.")
        _json_dump_map(save_folder / "errormap.json", _map)
    else:
        #Writes map to file
        next_map_number = int(map_number) + 1
        _logger.info("Writing map to %s.", save_folder / ("map" + str(map_number) + ".json"))
        _json_dump_map(save_folder / ("map" + str(map_number) + ".json"), _map)
        _logger.info("Updating map number to %s.", next_map_number)

        #Updating file
        with open(map_number_file, "r+", encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            lines[1] = str(next_map_number)
            for line in lines:
                file.write(line)

def entity_to_dictionary(obj:Entity) -> dict[str, Any]:
    '''Turns an entity into a dictionary representation'''
    changed_values = {}
    for attr, default_value in Entity.default_values.items():
        object_attribute = getattr(obj, attr)
        if not default_value and not object_attribute:
            #Checks if both the default and the attribute are falsy
            pass
        elif attr == 'name' and not object_attribute:
            #Checks if it's the name attribute because it's false by default
            #and the default values dictionary doesn't
            pass
        elif attr == 'shader' and object_attribute is Entity.default_shader:
            #Checks if shader is the default shader
            #(The default values dictionary just uses the names)
            pass
        elif object_attribute != default_value:
            changed_values[attr] = object_attribute
    return changed_values

def dictionary_to_entity(entity_dict:dict[str, Any]):
    '''Turns the entity dictionary back into the entity'''
    return Entity(**entity_dict)

if __name__ == "__main__":
    print(entity_to_dictionary(Entity()), "no value")
    print(entity_to_dictionary(Entity(model=Plane(subdivisions=[2,8]),scale= 50, color=color.white,texture="../../assets/textures/test123",rotation_x=0, y=0, collider = "box")), "yoru")
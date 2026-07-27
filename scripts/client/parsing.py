'''Parser for the client'''
import logging
from ast import literal_eval

_logger = logging.getLogger(__name__)

def parse_state(string:str):
    '''
    It parses the state string!
    I give up on the c implementation for now, just writing something fast in python for now
    Ideally this would be after serverside verification but uh, not happenning as of right now
    '''
    return_dict = {}
    position_list:list[tuple[float]] = []
    rotation_list:list[tuple[float]] = []
    try:
        #Index to traverse through list
        index:int = 1
        #Amount of cameras
        state_list:list[str] = string.split("\n")
        camera_amount:int = int(state_list[0])
        return_dict["cam_amount"] = camera_amount
        #Positions
        for _ in range(camera_amount):
            position_list.append(literal_eval(state_list[index]))
            index+=1
        return_dict["positions"] = position_list 
        #Rotation
        for _ in range(camera_amount):
            rotation_list.append(literal_eval(state_list[index]))
            index+=1
        return_dict["rotations"] = rotation_list
        #Whether player is shooting
        return_dict["is_shooting"] = literal_eval(state_list[index])
        index+=1
        #reload time
        return_dict["reload_time"] = float(state_list[index])
        index+=1
        #Whether it's dead
        return_dict["is_dead"] = literal_eval(state_list[index])
        index+=1
        #World position
        return_dict["world_pos"] = literal_eval(state_list[index])
        index+=1
        #Player rotation
        return_dict["player_rotation"] = literal_eval(state_list[index])
        index+=1
        #Player points
        return_dict["points"] = int(state_list[index])
        index +=1
        #In zone
        return_dict["in_zone"] = literal_eval(state_list[index])
        index +=1
        #shot someone
        return_dict["shot_someone"] = literal_eval(state_list[index])
        index += 1
        #Bullet trail rotatation
        return_dict["bullet_rotation"] = literal_eval(state_list[index]) #Could be None
        index += 1
        #Bullet scale length
        return_dict["bullet_scale"] = literal_eval(state_list[index]) #Could be None
        index += 1
        #Bullet position
        return_dict["bullet_pos"] = literal_eval(state_list[index])
        index += 1
        #Player round wins
        return_dict["round_wins"] = int(state_list[index])
        index += 1
        #NOTE: SERVER SIDED: Opponent ID
        return_dict["opponent_id"] = int(state_list[index])


    except IndexError as err:
        _logger.error("%s: String inputted %s is not correct", err, string)
    except ValueError as err:
        _logger.error("%s: Something went wrong with text parsing", err)
    return return_dict

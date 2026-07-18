from ursina import *
from scripts.in_game.player import *
player = get_player()

def send_info():
    cam_position_list = []
    cam_rotation_list = []

    if player.bullet_trail is not None and player.bullet_trail:
        return (str(player.perspective_list),
            str(player.bullet_trail),
            str(player.bullet_trail.world_position),
            str(player.reload_time),
            str(player.dead),
            str(player.world_position),
            str(player.rotation)
            )
    else:
        return (str(player.perspective_list),
            str(cam_position_list),
            str(cam_rotation_list),
            str("DNE"),
            str("DNE"),
            str(player.reload_time),
            str(player.dead),
            str(player.world_position),
            str(player.rotation)
            )
print(send_info())

def info_key():
    return  ("player cams: list[entity]",
               "player cams position: list[vec3]", 
               "player cams rotation: list[vec3]", 
               "bullet trail: entity",
               "bullet trail position: vec3",
               "reload time: float",
               "player dead: bool",
               "player world position: vec3",
               "player rotation: vec3",
               )
from ursina import *
from scripts.game.player import _Player
def send_info(player:_Player):
    cam_position_list:list[Vec3] = []
    cam_rotation_list:list[Vec3] = []
    for cam in player.perspective_list:
        cam_position_list.append(cam.world_position)
        cam_rotation_list.append(cam.rotation)

    if player.bullet_trail is not None and player.bullet_trail:
        return f'''{len(player.perspective_list)}
{"\n".join([str(tuple(x)) for x in cam_position_list])}
{"\n".join([str(tuple(x)) for x in cam_rotation_list])}
{True}
{player.reload_time}
{player.dead}
{tuple(player.world_position)}
{tuple(player.rotation)}
{player.points}
{player.in_zone}

'''

    return f'''{len(player.perspective_list)}
{"\n".join([str(tuple(x)) for x in cam_position_list])}
{"\n".join([str(tuple(x)) for x in cam_rotation_list])}
{False}
{player.reload_time}
{player.dead}
{tuple(player.world_position)}
{tuple(player.rotation)}
{player.points}
{player.in_zone}

'''

def info_key():
    return  ("amount of player cams",
               "player cams position: list[vec3]", 
               "player cams rotation: list[vec3]", 
               "shooting bullet: bool",
               "reload time: float",
               "player dead: bool",
               "player world position: vec3",
               "player rotation: vec3",
               "player points: boolean",
               "player in zone: boolean"
               )
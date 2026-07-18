from ursina import *
from scripts.in_game.player import _Player
def send_info(player:_Player):
    cam_position_list = []
    cam_rotation_list = []
    for cam in player.perspective_list:
        cam_position_list.append(cam.world_position)
        cam_rotation_list.append(cam.rotation)

    if player.bullet_trail is not None and player.bullet_trail:
        return (str(len(player.perspective_list)),
            str(cam_position_list),
            str(cam_rotation_list),  
            str(True), 
            str(player.reload_time),
            str(player.dead),
            str(player.world_position),
            str(player.rotation),
            str(player.points),
            str(player.in_zone)
            )
    else:
        return (str(len(player.perspective_list)),
            str(cam_position_list),
            str(cam_rotation_list),
            str(False),
            str(player.reload_time),
            str(player.dead),
            str(player.world_position),
            str(player.rotation),
            str(player.points),
            str(player.in_zone)
            )

def info_key():
    return  ("amount of player cams",
               "player cams position: list[vec3]", 
               "player cams rotation: list[vec3]", 
               "shooting bullet: bool"
               "reload time: float",
               "player dead: bool",
               "player world position: vec3",
               "player rotation: vec3",
               "player points: boolean",
               "player in zone: boolean"
               )
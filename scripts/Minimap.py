from ursina import *
from math import sin, cos, radians
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.player import _Player

class UpdateMinimap():
    def __init__(self,map_icon,real_entity,map_size):
        self.map_icon:Entity = map_icon
        self.real_entity:Entity = real_entity
        self.map_size:int = map_size
        #icons on the minimap
    def minimap_update(self) -> None:
        self.map_icon.x = self.real_entity.x / self.map_size
        self.map_icon.y = self.real_entity.z / self.map_size
class MinimapIcons:
    def __init__(self, player:_Player):
        self.minimap:Entity = Entity(scale=(0.2,0.2), x = 0.7, y= 0.4, model = "quad", texture="map_1", parent = camera.ui)
        self.player_icon:Entity = Entity(parent = self.minimap, texture = "red_dot", scale = 0.05, model = "quad", z =-0.5, color=color.red)
        self.square_icon:Entity = Entity(parent = self.minimap, scale = 0.05, model = "quad", z =-0.5)
        self.vision_cone_icon:Entity = Entity(scale = (4,0.2), parent= self.player_icon, model = "quad", z = -1, color = color.red, origin = (0.5,0), a = 0.4 )
        self.vision_cone_icon1:Entity = Entity(scale = (4,0.2), parent= self.player_icon, model = "quad", z = -1, color = color.red, origin = (0.5,0), a = 0.4 )
        self.player = player
    def vision_cone(self):
        left_angle = radians(self.player.rotation_y - 135)
        right_angle = radians(self.player.rotation_y - 45)
        left_dir = Vec3(sin(left_angle), 0, cos(left_angle))
        right_dir = Vec3(sin(right_angle), 0, cos(right_angle))


        self.left_bound = raycast(origin = self.player.world_position, direction = left_dir, ignore = [self.player], distance = 100, debug = True)
        self.right_bound = raycast(origin = self.player.world_position, direction =  right_dir, ignore = [self.player], distance = 100, debug = True)
        self.vision_cone_icon.scale = (self.left_bound.distance/2, 0.2)
        self.vision_cone_icon1.scale = (self.right_bound.distance/2, 0.2)

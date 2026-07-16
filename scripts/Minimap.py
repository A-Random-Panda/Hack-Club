from ursina import *

class UpdateMinimap():
    def __init__(self,map_icon,real_entity,map_size):
        self.map_icon:Entity = map_icon
        self.real_entity:Entity = real_entity
        self.map_size:int = map_size
        #icons on the minimap
    def minimap_update(self):
        self.map_icon.x = self.real_entity.x / self.map_size
        self.map_icon.y = self.real_entity.z / self.map_size
class MinimapIcons:
    def __init__(self):
        self.minimap:Entity = Entity(scale=(0.2,0.2), x = 0.7, y= 0.4, model = "quad", texture="map_1", parent = camera.ui)
        self.player_icon:Entity = Entity(parent = self.minimap, texture = "red_dot", scale = 0.05, model = "quad", z =-0.5, color=color.red)
        self.square_icon = Entity(parent = self.minimap, scale = 0.05, model = "quad", z =-0.5)
        self.vision_cone_icon = Entity(scale = (4,0.2), parent= self.player_icon, model = "quad", z = -1, color = color.red, origin = (0.7,0), a = 0.4 )



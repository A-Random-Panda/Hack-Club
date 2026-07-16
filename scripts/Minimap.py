from ursina import Entity

class UpdateMinimap():
    def __init__(self,map_icon,real_entity,map_size):
        self.map_icon:Entity = map_icon
        self.real_entity:Entity = real_entity
        self.map_size:int = map_size
    def minimap_update(self):
        self.map_icon.x = self.real_entity.x / self.map_size
        self.map_icon.y = self.real_entity.z / self.map_size



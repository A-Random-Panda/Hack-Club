from ursina import *
class KOTH:
    def __init__(self,objective_length):
        self.objective_length = objective_length
        self.obj_wallN = Entity(model="cube", scale=(50,12,1), color=color.red, collider = "box", x=0, z=-25)
        self.obj_wall = Entity(model="cube", scale=(50,12,1), color=color.green, collider = "box", x=0, z=25)
        wall3 = Entity(model="cube", scale=(50,12,1), color=color.blue, collider = "box", x=-25, z=0, rotation_y=90)
        wall4 = Entity(model="cube", scale=(50,12,1), color=color.black, collider = "box", x=25, z=0, rotation_y=90)
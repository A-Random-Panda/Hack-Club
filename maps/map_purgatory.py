'''This is the first map made, future maps may or may not be in JSON format'''

#This won't be in the main i
from ursina import *

class Purgatory():
    map_loaded = False
    entity_list:list[Entity] = []

    @classmethod
    def load_map(cls):
        '''How this will work is that static entities won't have a name while other entities will.'''
        cls.map_loaded = True
        cls.entity_list = [
        Entity(model=Plane(subdivisions=[2,8]),scale= 100, texture='test123', color=color.white, collider = "box") #floor
        ]

    @classmethod
    def unload_map(cls):
        cls.map_loaded = False
        for i in cls.entity_list:
            destroy(i)

    @classmethod
    def update(cls):
        pass

if __name__ == "__main__":
    from ursina.prefabs.first_person_controller import FirstPersonController
    from sys import exit

    application.asset_folder = Path(r"../assets")
    app = Ursina()

    fpc = FirstPersonController(
        speed = 16,
        jump_height= 4,
        collider="box",
        gravity= 1,
        enabled = True)

    Purgatory.load_map()

    def input(key):
        if key == "escape":
            exit(0)
        if key == "1":
            Purgatory.unload_map()
        if key == "2":
            Purgatory.load_map()

    def update():
        Purgatory.update()
        if fpc.y_getter() < -10:
            fpc.position_setter((0, 10, 0))

    app.run()
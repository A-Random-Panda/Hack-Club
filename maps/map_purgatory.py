'''This is the first map made, future maps may or may not be in JSON format'''

from ursina import *

class Purgatory():
    '''Helper class for the purgatory class'''
    map_loaded = False
    entity_list:list[Entity] = []

    @classmethod
    def load_map(cls):
        '''
        Method to load the map.
        Eventually, it probably is better to put split objects together
        '''
        if cls.map_loaded:
            return
        cls.map_loaded = True
        cls.entity_list = [
        #Floor
        Entity(model="cube", scale=(600, 1, 400), texture='purg_floor', color=color.white, collider="box"),

        #Roof
        Entity(model="cube", scale=(600, 1, 400), y=20, texture='purg_roof', color=color.white, collider="box"),

        #Walls across x axis
        Entity(model="cube", scale=(500, 20, 10), position=(0, 10, 200), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(500, 20, 10), position=(0, 10, -200), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(50, 20, 10), position=(275.0, 10, 25.0), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(50, 20, 10), position=(275.0, 10, -25.0), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(50, 20, 10), position=(-275.0, 10, 25.0), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(50, 20, 10), position=(-275.0, 10, -25.0), texture='purg_bound', color=color.white, collider="box"),

        #Walls across z axis
        Entity(model="cube", scale=(10, 20, 175.0), position=(250, 10, 112.5), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 20, 175.0), position=(250, 10, -112.5), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 20, 175.0), position=(-250, 10, 112.5), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 20, 175.0), position=(-250, 10, -112.5), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 20, 50), position=(300, 10, 0), texture='purg_bound', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 20, 50), position=(-300, 10, 0), texture='purg_bound', color=color.white, collider="box"),

        #near spawn walls
        Entity(model="cube", scale=(10, 10, 150), position=(200, 5, 0), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 10, 150), position=(-200, 5, 0), texture='purg_wall', color=color.white, collider="box"),

        #Closer walls across z axis
        Entity(model="cube", scale=(10, 10, 100), position=(150, 5, 100), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 10, 100), position=(-150, 5, 100), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 10, 100), position=(150, 5, -100), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(10, 10, 100), position=(-150, 5, -100), texture='purg_wall', color=color.white, collider="box"),

        #Closer walls across x axis point walls
        Entity(model="cube", scale=(125.0, 10, 10), position=(87.5, 5, 150), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(125.0, 10, 10), position=(-87.5, 5, 150), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(125.0, 10, 10), position=(87.5, 5, -150), texture='purg_wall', color=color.white, collider="box"),
        Entity(model="cube", scale=(125.0, 10, 10), position=(-87.5, 5, -150), texture='purg_wall', color=color.white, collider="box")
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
    from ursina.prefabs.editor_camera import EditorCamera
    from sys import exit

    application.asset_folder = Path(r"../assets")
    app = Ursina()

    coordinate_text = Text(scale=1, position = (-.5*1.778, .5), origin = (-.5, .5))

    player_shadow = Entity(model="Better_Tank", color=color.red,scale = 0.5, collider="mesh", enabled=False)
    player_line = Entity(model = Quad(radius=200, mode='line'), color=color.white, enabled=False)

    fpc = FirstPersonController(
        speed = 16,
        jump_height= 4,
        collider="box",
        gravity= 1,
        enabled = True)

    editor_camera = EditorCamera(enabled=False, move_speed=50)

    Purgatory.load_map()

    def input(key):
        if key == "escape":
            exit(0)
        if key == "1":
            Purgatory.unload_map()
        if key == "2":
            Purgatory.load_map()
        if key == 'tab':
            if fpc.enabled:
                fpc.disable()
                player_shadow.enable()
                player_line.enable()
                editor_camera.position = fpc.position
                editor_camera.enable()
            else:
                editor_camera.disable()
                player_shadow.disable()
                player_line.disable()
                fpc.position = editor_camera.position
                fpc.enable()
        if key == "shift":
            fpc.speed = 8
        if key == "shift up":
            fpc.speed = 16

    def update():
        Purgatory.update()
        if editor_camera.enabled:
            player_line.position = editor_camera.position
            player_shadow.position = editor_camera.position
            player_line.rotation = editor_camera.rotation
            coordinate_text.text = editor_camera.position
        else:
            coordinate_text.text = fpc.position
        if fpc.y_getter() < -10:
            fpc.position_setter((0, 10, 0))

    app.run()
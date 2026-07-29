from __future__ import annotations
from ursina import *
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.game.player import _Player
    from scripts.game.ui import UIController
    from scripts.game.audio_controller import AudioController
class KOTH:
    def __init__(self,player:"_Player",objective_length:int,location_x:int,location_z:int,ui:UIController,audio:AudioController):
        self.objective_length = objective_length
        self.ui = ui
        self.audio = audio
        self.location_z:int = location_z
        self.location_x:int = location_x
        self.player:_Player = player
        self.obj_wall1 = Entity(model="cube", scale=(self.objective_length+0.5,1.1,0.5), color=color.yellow, x=self.location_x, z=self.location_z - self.objective_length/2)
        self.obj_wall2 = Entity(model="cube", scale=(self.objective_length+0.5,1.1,0.5), color=color.yellow, x=self.location_x, z=self.location_z + self.objective_length/2)
        self.obj_wall3 = Entity(model="cube", scale=(self.objective_length+0.5,1.1,0.5), color=color.yellow, x=self.location_x - self.objective_length/2, z=self.location_z, rotation_y=90)
        self.obj_wall4 = Entity(model="cube", scale=(self.objective_length+0.5,1.1,0.5), color=color.yellow, x=self.location_x + self.objective_length/2, z=self.location_z, rotation_y=90)
        self.time_inside:float = 0.0
    def within_zone(self) -> None:
        within_confines = (self.location_z + self.objective_length/2) >= self.player.z >= (self.location_z - self.objective_length/2) and (self.location_x+self.objective_length/2) >= self.player.x >= (self.location_x - self.objective_length/2)
        if within_confines and not self.player.in_zone:
            self.player.in_zone = True
            self.time_inside = time.perf_counter()
        elif not within_confines:
            self.player.in_zone = False
    def gain_points(self,points,names,round_wins) -> None:
        if self.player.in_zone:
            if 1.5 < abs(time.perf_counter()-self.time_inside):
                self.time_inside = time.perf_counter()
                self.player.points += 10
                self.audio.success.play()
                print(self.player.points)
                self.ui.leaderboard_text.text = f"{self.player.points} {self.player.username} \n round wins: {self.player.round_wins}"
                self.ui.enemy_leaderboard_text.text = f"{points} {names.strip(self.player.username)} \n round wins: {round_wins}"   
    def update_zone(self):
        destroy(self.obj_wall2)
        destroy(self.obj_wall3)
        destroy(self.obj_wall4)
        destroy(self.obj_wall1)
        self.obj_wall1 = Entity(model="cube", scale=(self.objective_length+0.5,2,0.5), color=color.yellow,  x=self.location_x, z=self.location_z - self.objective_length/2)
        self.obj_wall2 = Entity(model="cube", scale=(self.objective_length+0.5,2,0.5), color=color.yellow,  x=self.location_x, z=self.location_z + self.objective_length/2)
        self.obj_wall3 = Entity(model="cube", scale=(self.objective_length+0.5,2,0.5), color=color.yellow,  x=self.location_x - self.objective_length/2, z=self.location_z, rotation_y=90)
        self.obj_wall4 = Entity(model="cube", scale=(self.objective_length+0.5,2,0.5), color=color.yellow,  x=self.location_x + self.objective_length/2, z=self.location_z, rotation_y=90)
    
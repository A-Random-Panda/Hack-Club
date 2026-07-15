import time
from scripts.player import _Player
from ursina import Entity, Text, Audio

RESPAWN_TIME = 5

class DeathManager():
    def __init__(self, player, menu_overlay, stop_audio, death_sound, respawn_text, player_shadow, cam_switching):
        self.player:_Player = player
        self.menu_overlay:Entity = menu_overlay
        self.stop_audio:Audio = stop_audio
        self.death_sound = death_sound
        self.respawn_text:Text = respawn_text
        self.player_shadow:Entity = player_shadow
        self.cam_switching = cam_switching
    def kill(self):
        self.stop_audio()
        self.death_sound.play()
        self.player.enabled = False
        self.player.dead = True
        self.player.death_timer = time.perf_counter()
        self.player.input_enabled = False
        self.menu_overlay.enabled = True
        self.respawn_text.enabled = True
        print("dead")
    def while_dead(self):
        print("still dead")
        timer = "Respawning in " + str(round(RESPAWN_TIME - time.perf_counter() + self.player.death_timer, 1))
        self.respawn_text.text = timer
        self.respawn_text.enabled = True
        self.player_shadow.enabled = False
    def respawned(self):
        self.player.dead = False
        print("alive")
        self.player.input_enabled = True
        self.player.enabled = True
        self.respawn_text.enabled = False
        self.menu_overlay.enabled = False
        self.cam_switching()
        self.player.position = (0.5, 1.0,0.5)
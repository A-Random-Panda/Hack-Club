import time
from scripts.player import _Player
from ursina import Entity, Text, Audio
from scripts.audio_controller import AudioController

RESPAWN_TIME = 5
RESPAWN_POSITION = (0.5, 1.0,0.5)

class DeathManager():
    def __init__(self, player, menu_overlay, audio, respawn_text, player_shadow, cam_switching):
        self.player:_Player = player
        self.audio:AudioController = audio
        self.menu_overlay:Entity = menu_overlay
        self.respawn_text:Text = respawn_text
        self.player_shadow:Entity = player_shadow
        self.cam_switching = cam_switching
    def kill(self) -> None:
        self.audio.stop_audio()
        self.audio.death.play()
        self.player.enabled = False
        self.player.dead = True
        self.player.death_timer = time.perf_counter()
        self.player.input_enabled = False
        self.respawn_text.enabled = True
        print("dead")
    def while_dead(self) -> None:
        print("still dead")
        timer = "Respawning in " + str(round(RESPAWN_TIME - time.perf_counter() + self.player.death_timer, 1))
        self.respawn_text.text = timer
        self.respawn_text.enabled = True
        self.player_shadow.enabled = False
        self.menu_overlay.enabled = True
    def respawned(self) -> None:
        self.player.dead = False
        print("alive")
        self.player.input_enabled = True
        self.player.enabled = True
        self.respawn_text.enabled = False
        self.menu_overlay.enabled = False
        self.cam_switching()
        self.player.position = RESPAWN_POSITION
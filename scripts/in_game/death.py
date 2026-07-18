import time
from ursina import Entity
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController



RESPAWN_TIME = 5
RESPAWN_POSITION = (0.5, 1.0,0.5)

class DeathManager():
    def __init__(self, player, audio, ui, player_shadow, cam_switching):
        self.player:_Player = player
        self.audio:AudioController = audio
        self.ui:UIController = ui
        self.player_shadow:Entity = player_shadow
        self.cam_switching = cam_switching
    def kill(self) -> None:
        self.audio.stop_audio()
        self.audio.death.play()
        self.player.enabled = False
        self.player.dead = True
        self.player.death_timer = time.perf_counter()
        self.player.input_enabled = False
        self.ui.respawn_text.enabled = True
        print("dead")
    def while_dead(self) -> None:
        print("still dead")
        timer = "Respawning in " + str(round(RESPAWN_TIME - time.perf_counter() + self.player.death_timer, 1))
        self.ui.respawn_text.text = timer
        self.ui.respawn_text.enabled = True
        self.player_shadow.enabled = False
        self.ui.menu_overlay.enabled = True
    def respawned(self) -> None:
        self.player.dead = False
        print("alive")
        self.player.input_enabled = True
        self.player.enabled = True
        self.ui.respawn_text.enabled = False
        self.ui.menu_overlay.enabled = False
        self.cam_switching()
        self.player.position = RESPAWN_POSITION
        self.ui.close_all_uis()

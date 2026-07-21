from ursina import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController
def start_game(self,player:"_Player",audio:"AudioController",ui:"UIController"):
    player.position = player.respawn_point
    player.cash = 1000
    ui.close_all_uis()
    player.reload_time = 5
    player.points = 0
    player.max_cams = 5
    player.reload_time = 5

    pass
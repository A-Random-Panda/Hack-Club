from ursina import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController

class MainMenu:
    def __init__(self, player:_Player, audio: AudioController, ui: UIController):
        self.player = player
        self.audio = audio
        self.ui = ui
        self.background = Entity(model="quad", scale = (2,2),color = color.black, enabled = False)
    def open_main_menu(self, boolean= True) -> None:
        self.ui.background.enabled = boolean
        self.ui.mouse_in_menu(boolean)
    def player_main_menu(self, boolean = False) -> None:
        self.player.in_main_menu = boolean
        self.open_main_menu(boolean)
        self.ui.open_game_button.enabled = boolean

        
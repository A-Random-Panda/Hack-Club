from __future__ import annotations
from ursina import *
from typing import TYPE_CHECKING
from random import randint
from scripts.game.settings import DEFAULT_NAMES
if TYPE_CHECKING:
    from scripts.game.player import _Player
    from scripts.game.audio_controller import AudioController
    from scripts.game.ui import UIController

class MainMenu:
    def __init__(self, player:_Player, audio: AudioController, ui: UIController):
        self.player = player
        self.audio = audio
        self.ui = ui
        self.background = Entity(model="quad", scale = (2,2),color = color.black, enabled = False)
    
    def open_main_menu(self, boolean= True) -> None:
        self.ui.background.enabled = boolean
        self.ui.mouse_in_menu(boolean)
        self.ui.name_input.enabled = boolean
        if boolean == False:
            if self.ui.name_input.text.strip(" ") == "" or self.ui.name_input.text == self.ui.name_input.default_value:
                self.player.username = DEFAULT_NAMES[randint(0,29)]
            else:
                self.player.username = self.ui.name_input.text
        self.ui.leaderboard_text.text = f"{self.player.points} {self.player.username}"
    
    def player_main_menu(self, boolean = False) -> None:
        self.player.in_main_menu = boolean
        self.open_main_menu(boolean)
        self.ui.open_game_button.enabled = boolean
        self.ui.map_selector_button.enabled = boolean
        self.ui.name_input.enabled = boolean
        self.ui.join_friend_button.enabled = boolean
        self.ui.join_game_button.enabled = False

    
    def map_selector(self, boolean = True):
        self.ui.open_game_button.enabled = not boolean
        self.ui.map_selector_button.enabled = not boolean
        self.ui.map_selector_text.enabled = boolean
        self.ui.back_to_main_button.enabled = boolean
        self.ui.name_input.enabled = not boolean
        self.ui.join_friend_button.enabled = not boolean
    
    def join_game(self, boolean = True):
        self.ui.open_game_button.enabled = not boolean
        self.ui.map_selector_button.enabled = not boolean
        self.ui.back_to_main_button.enabled = boolean
        self.ui.name_input.enabled = not boolean
        self.ui.join_friend_button.enabled = not boolean
        self.ui.host_input.enabled = boolean
        self.ui.port_input.enabled = boolean
        self.ui.port_text.enabled = boolean
        self.ui.join_game_button.enabled = boolean

    def switch_back(self):
        self.join_game(False)
        self.map_selector(False)
        self.player_main_menu(True)




        
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
    
    def open_main_menu(self, open_state= True) -> None:
        self.ui.background.enabled = open_state
        self.ui.mouse_in_menu(open_state)
        self.ui.name_input.enabled = open_state
        if not open_state:
            if self.ui.name_input.text.strip(" ") == "" or self.ui.name_input.text == self.ui.name_input.default_value:
                self.player.username = DEFAULT_NAMES[randint(0,29)]
            else:
                self.player.username = self.ui.name_input.text
        self.ui.leaderboard_text.text = f"{self.player.points} {self.player.username}"

    def player_main_menu(self, open_state = False) -> None:
        self.player.in_main_menu = open_state
        self.open_main_menu(open_state)
        self.ui.host_game_button.enabled = open_state
        self.ui.open_game_button.enabled = open_state
        self.ui.map_selector_button.enabled = open_state
        self.ui.name_input.enabled = open_state
        self.ui.join_friend_button.enabled = open_state
        self.ui.start_server_button.disable()
        self.ui.join_game_button.disable()
        self.ui.has_window_checkbox.disable()
        self.ui.has_window_text.disable()

    def map_selector(self, open_state = True):
        self.ui.host_game_button.enabled = not open_state
        self.ui.open_game_button.enabled = not open_state
        self.ui.map_selector_button.enabled = not open_state
        self.ui.map_selector_text.enabled = open_state
        self.ui.back_to_main_button.enabled = open_state
        self.ui.name_input.enabled = not open_state
        self.ui.join_friend_button.enabled = not open_state

    def join_game(self, open_state = True):
        self.ui.host_game_button.enabled = not open_state
        self.ui.open_game_button.enabled = not open_state
        self.ui.map_selector_button.enabled = not open_state
        self.ui.back_to_main_button.enabled = open_state
        self.ui.name_input.enabled = not open_state
        self.ui.join_friend_button.enabled = not open_state
        self.ui.host_input.enabled = open_state
        self.ui.port_input.enabled = open_state
        self.ui.port_text.enabled = open_state
        self.ui.join_game_button.enabled = open_state
        if self.ui.port_input.text.strip() == "":
            self.ui.port_input.text = self.ui.port_input.default_value
        if self.ui.host_input.text.strip() == "":
            self.ui.host_input.text = self.ui.host_input.default_value

    def host_game(self, open_state = True):
        self.ui.host_game_button.enabled = not open_state
        self.ui.open_game_button.enabled = not open_state
        self.ui.map_selector_button.enabled = not open_state
        self.ui.back_to_main_button.enabled = open_state
        self.ui.name_input.enabled = not open_state
        self.ui.join_friend_button.enabled = not open_state
        self.ui.host_input.enabled = not open_state
        self.ui.join_game_button.enabled = not open_state
        self.ui.port_input.enabled = open_state
        self.ui.port_text.enabled = open_state
        self.ui.start_server_button.enabled = open_state
        self.ui.has_window_checkbox.enabled = open_state
        self.ui.has_window_text.enabled = open_state

        if self.ui.port_input.text.strip() == "":
            self.ui.port_input.text = self.ui.port_input.default_value

    def switch_back(self):
        self.join_game(False)
        self.map_selector(False)
        self.player_main_menu(True)

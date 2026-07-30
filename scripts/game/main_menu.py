from __future__ import annotations
from enum import Enum, auto
from typing import TYPE_CHECKING
from sys import exit
from logging import getLogger

from ursina import *

if TYPE_CHECKING:
    from logging import Logger
    from scripts.game.player import _Player
    from scripts.game.audio_controller import AudioController
    from scripts.game.ui import UIController

_logger:Logger = getLogger(__name__)

class _Screens(Enum):
    GAME = auto()
    MAIN_MENU = auto()
    MAP_SELECTOR = auto()
    JOIN_GAME = auto()
    HOST_GAME = auto()
    LOBBY = auto()

class MainMenu:
    def __init__(self, player:_Player, audio: AudioController, ui: UIController):
        self.player = player
        self.audio = audio
        self.ui = ui
        self.current_screen = _Screens.MAIN_MENU

    def _enable_main_menu_elements(self):
        '''Enables all elements that are a part of the main menu'''
        self.ui.host_game_button.enable()
        self.ui.open_game_button.enable()
        self.ui.rules_button.enable()
        self.ui.name_input.enable()
        self.ui.exit_game_button.enable()
        self.ui.join_friend_button.enable()
        self.ui.lobby_botton.enable()
        self.ui.title.enable()

    def _disable_main_menu_elements(self):
        '''Disables all elements in the main menu'''
        self.ui.host_game_button.disable()
        self.ui.open_game_button.disable()
        self.ui.rules_button.disable()
        self.ui.name_input.disable()
        self.ui.exit_game_button.disable()
        self.ui.join_friend_button.disable()
        self.ui.lobby_botton.disable()
        self.ui.title.disable()

    def _enter_subscreen(self):
        '''Disables all the elements shown on the main menu, and enables the back button'''
        self._disable_main_menu_elements()
        self.ui.back_to_main_button.enable()

    def exit_subscreen(self):
        '''Disables the elements in the current subscreen, and returns to the main menu'''
        #Disables elements depending on current open screen
        self.ui.background.texture = "menu_screen"
        match self.current_screen:
            case _Screens.MAIN_MENU:
                _logger.error("Current screen detected as main menu while attempting to exit subscreen")
            case _Screens.GAME:
                _logger.error("Current screen detected as in game while attempting to exit subscreen")
                return
            case _Screens.MAP_SELECTOR:
                self.ui.rules_button.disable()
                self.ui.map_selector_text.disable()
            case _Screens.JOIN_GAME:
                self.ui.host_input.disable()
                self.ui.port_input.disable()
                self.ui.port_text.disable()
                self.ui.join_game_button.disable()
                self.ui.hostname_text.disable()
                self.ui.disconnect_button.disable()
            case _Screens.HOST_GAME:
                self.ui.port_input.disable()
                self.ui.port_text.disable()
                self.ui.start_server_button.disable()
                self.ui.server_text.disable()
                self.ui.has_window_checkbox.disable()
                self.ui.has_window_text.disable()
                self.ui.auto_join_checkbox.disable()
                self.ui.auto_join_text.disable()
                self.ui.disconnect_button.disable()
                self.ui.stop_server_button.disable()
            case _Screens.LOBBY:
                self.ui.start_game_button.disable()
                self.ui.lobby_text.disable()
                self.ui.disconnect_button.disable()
                self.ui.stop_server_button.disable()
            case _:
                _logger.error("Current screen unknown, entering main menu")

        #Enable main menu elements
        self.current_screen = _Screens.MAIN_MENU
        self._enable_main_menu_elements()
        self.ui.back_to_main_button.disable()

    def _initialize_player(self) -> None:
        '''Enables the player and initializes things needed for the game'''
        self.player.enable()
        self.player.in_main_menu = False
        self.ui.background.disable()
        self.ui.title.disable()
        self.ui.set_mouse_game_state()
        self.ui.acquire_and_set_name()
        self.ui.leaderboard_text.text = f"{self.player.points} {self.player.username} \n round wins: {self.player.round_wins}"
        self.ui.enemy_leaderboard_text.text = f""

    def _disable_player(self) -> None:
        '''
        Disables player, enables background
        Might resest points, but I'll see later
        Probably better to just have a general cleanup function
        '''
        self.player.disable()
        self.ui.background.enable()
        self.ui.title.enable()
        self.ui.set_mouse_menu_state()
        self.player.in_main_menu = True
        if self.player.username:
            self.ui.name_input.text = self.player.username

    def enter_game(self) -> None:
        '''Closes the main menu and starts the game'''
        self._initialize_player()
        self._disable_main_menu_elements()
        self.current_screen = _Screens.GAME

    def open_main_menu(self) -> None:
        '''Opens the main menu'''
        self._disable_player()
        self._enable_main_menu_elements()
        self.current_screen = _Screens.MAIN_MENU

    def open_rules_menu(self):
        '''Opens the map selector menu'''
        self._enter_subscreen()
        self.ui.background.texture = ""
        self.ui.background.color = color.white
        self.current_screen = _Screens.MAP_SELECTOR
        self.ui.rules_button.disable()
        self.ui.map_selector_text.enable()

    def open_join_game(self):
        '''Opens the join game menu'''
        self._enter_subscreen()
        self.current_screen = _Screens.JOIN_GAME
        self.ui.host_input.enable()
        self.ui.port_input.enable()
        self.ui.port_text.enable()
        self.ui.join_game_button.enable()
        self.ui.hostname_text.enable()
        self.ui.disconnect_button.enable()
        #Switches back if to default if the text box is blank
        if self.ui.port_input.text.strip() == "":
            self.ui.port_input.text = self.ui.port_input.default_value
        if self.ui.host_input.text.strip() == "":
            self.ui.host_input.text = self.ui.host_input.default_value

    def open_host_game(self):
        '''Opens the host game menu'''
        self._enter_subscreen()
        self.current_screen = _Screens.HOST_GAME
        self.ui.port_input.enable()
        self.ui.port_text.enable()
        self.ui.start_server_button.enable()
        self.ui.server_text.enable()
        self.ui.has_window_checkbox.enable()
        self.ui.has_window_text.enable()
        self.ui.auto_join_checkbox.enable()
        self.ui.auto_join_text.enable()
        self.ui.disconnect_button.enable()
        self.ui.stop_server_button.enable()
        #Switches back if to default if the text box is blank
        if self.ui.port_input.text.strip() == "":
            self.ui.port_input.text = self.ui.port_input.default_value

    def open_lobby(self):
        '''Opens the host game menu'''
        self._enter_subscreen()
        self.current_screen = _Screens.LOBBY
        self.ui.start_game_button.enable()
        self.ui.lobby_text.enable()
        self.ui.disconnect_button.enable()
        self.ui.stop_server_button.enable()

    def normal_exit(self):
        '''Exit with 0 host code'''
        exit(0)

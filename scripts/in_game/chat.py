from ursina import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController


class Chat:
    def __init__(self, player:_Player, ui:UIController, audio:AudioController):
        self.player = player
        self.ui = ui
        self.audio = audio
        self.chat_list = []

    def max_chat(self):
        if len(self.chat_list) > 4:
            self.chat_list.pop
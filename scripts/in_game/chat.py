from ursina import *
from typing import TYPE_CHECKING
import time
if TYPE_CHECKING:
    from scripts.in_game.player import _Player
    from scripts.in_game.audio_controller import AudioController
    from scripts.in_game.ui import UIController


class ChatController:
    def __init__(self, player:_Player, ui:UIController, audio:AudioController):
        self.player = player
        self.ui = ui
        self.audio = audio
        self.chat_list:list[Text] = []

    def chat(self):
        if len(self.chat_list) > 4:
            destroy(self.chat_list.pop(0))
        
        if 4 < abs(time.perf_counter()- self.player.chat_opened):
            for msg in range (len(self.chat_list)):
                self.chat_list[msg].enabled = False
                self.ui.chat_overlay.enabled = False

        else:
            for msg in range (len(self.chat_list)):
                self.chat_list[msg].y = -.2 - 0.05 * (msg)
                self.chat_list[msg].enabled = True
                self.ui.chat_overlay.enabled = True

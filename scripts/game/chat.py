from __future__ import annotations
from ursina import *
from typing import TYPE_CHECKING
import time
if TYPE_CHECKING:
    from scripts.game.audio_controller import AudioController
    from scripts.game.ui import UIController


class ChatController:
    def __init__(self, ui:UIController, audio:AudioController):
        self.ui = ui
        self.audio = audio
        self.chat_list:list[Text] = []
        self.chat_opened_time = -1

    def start_chat_timer(self) -> None:
        '''Starts the timer used to close the chat'''
        self.chat_opened_time = time.perf_counter()

    def chat(self):
        if len(self.chat_list) > 4:
            destroy(self.chat_list.pop(0))
        if 4 < abs(time.perf_counter() - self.chat_opened_time):
            for msg in range (len(self.chat_list)):
                self.chat_list[msg].enabled = False
                self.ui.chat_overlay.enabled = False

        else:
            for msg in range (len(self.chat_list)):
                self.chat_list[msg].y = -.2 - 0.05 * (msg)
                self.chat_list[msg].enabled = True
                self.ui.chat_overlay.enabled = True

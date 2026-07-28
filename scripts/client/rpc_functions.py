'''
This module contains the RPC functions needed to run the game

RPC basically is the call from a peer to run a rpc function on the other peer's computer
'''
from logging import getLogger
from typing import Any, TYPE_CHECKING
from ursina.networking import *
from ursina.text import Text, color

if TYPE_CHECKING:
    from scripts.game.ui import UIController
    from scripts.game.main_menu import MainMenu
    from scripts.game.chat import ChatController

_logger = getLogger(__name__)
peer:RPCPeer = RPCPeer()

class GameState():
    '''Variables relating to the game state'''

    @classmethod
    def reset(cls) -> None:
        '''Resets the gamestate to default'''
        cls.game_started = False
        cls.opponent_disconnected = False
        cls.state_string:str = ""
        cls.game_state:dict[str, Any] = {}
        cls.opponent_name:str = ""
        cls.id:int = 0

    ui_controller:"UIController | None" = None
    main_menu:"MainMenu | None" = None
    chat:"ChatController | None" = None
    @classmethod
    def set_ui_controller(cls, controller:"UIController") -> None:
        '''Sets the ui controller, meant to be used in initialization'''
        cls.ui_controller = controller
    @classmethod
    def set_main_menu(cls, menu:"MainMenu") -> None:
        '''Sets the ui controller, meant to be used in initialization'''
        cls.main_menu = menu
    @classmethod
    def set_chat(cls, chat:"ChatController") -> None:
        '''Sets the ui controller, meant to be used in initialization'''
        cls.chat = chat

GameState.reset()

@rpc(peer)
def state_to_client(connection, time_received, state:str):
    '''Receives the game state from the server'''
    GameState.state_string = state

@rpc(peer)
def names_to_client(connection, time_received, name:str):
    assert GameState.ui_controller is not None
    GameState.ui_controller.lobby_text.text = f"Connected_Users:\n{name}"
    GameState.opponent_name = name

@rpc(peer)
def game_started_state(connection, time_received, game_start:bool):
    '''Controls whether the game has started or not'''
    assert GameState.main_menu is not None
    if game_start:
        GameState.game_started = True
        GameState.opponent_disconnected = False
        GameState.main_menu.exit_subscreen()
        GameState.main_menu.enter_game()
    else:
        pass

@rpc(peer)
def alert_opponent_disconnected(connection, time_received):
    '''Alerts the client that the opponent disconnected'''
    GameState.opponent_disconnected = True

@rpc(peer)
def id_to_client(connection, time_received, _id:int):
    '''Gets your own id'''
    GameState.id = _id

@rpc(peer)
def send_chat_message(connection, time_received, message:str):
    assert GameState.chat is not None
    GameState.chat.chat_list.append(Text(text = message,
                              origin = (0.8,0),
                              position = (0.8,0,-2),
                              scale = 0.75,
                              color=color.white,
                              enabled = True))
    GameState.chat.start_chat_timer()

@rpc(peer)
def on_connect(connection, time_connected):
    '''
    On connection to the server
    Currently logs it to the console
    '''
    assert GameState.ui_controller is not None
    assert GameState.main_menu is not None
    GameState.ui_controller.show_temp_text("You were connected to a server!")
    peer.name_to_server(peer.get_connections()[0], GameState.ui_controller.acquire_and_set_name())
    GameState.main_menu.exit_subscreen()
    GameState.main_menu.open_lobby()

@rpc(peer)
def on_disconnect(connection, time_disconnected):
    '''
    Runs on disconnection to the server
    Currently logs it to the console.
    '''
    assert GameState.ui_controller is not None
    GameState.ui_controller.show_temp_text("You were disconnected from the server at %s!", time_disconnected)

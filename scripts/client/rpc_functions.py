'''
This module contains the RPC functions needed to run the game

RPC basically is the call from a peer to run a rpc function on the other peer's computer
'''

from logging import getLogger
from typing import Any
from ursina.networking import *


_logger = getLogger(__name__)
peer:RPCPeer = RPCPeer()

class GameState():
    '''Variables relating to the game state'''
    game_started = False
    state_string:str = ""
    game_state:dict[str, Any] = {}

@rpc(peer)
def state_to_client(connection, time_received, state:str):
    '''Receives the game state from the server'''
    GameState.state_string = state

@rpc(peer)
def game(connection, time_received, gamestate:bool):
    '''Controls whether the game has started or not'''
    GameState.game_started = gamestate

@rpc(peer)
def on_connect(connection, time_connected):
    '''
    On connection to the server
    Currently logs it to the console
    '''
    _logger.info("You were connected to a server!")

@rpc(peer)
def on_disconnect(connection, time_disconnected):
    '''
    Runs on disconnection to the server
    Currently logs it to the console.
    '''
    _logger.info("You were disconnected from the server at %s!", time_disconnected)

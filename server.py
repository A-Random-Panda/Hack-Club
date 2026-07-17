'''
This file is for testing a multiplayer implementation of Ursina without modifying the main game file

Things to think about:
Ursina uses TCP, but it might be worth it to use something with UDP instead
if latency ever becomes an issue 

Multiplayer method
2. Sending game state
4. Server authoritive
6. Snapshot Interpolation
I think the best way is to just to send gamestate and do snapshop interpolation
It might take a while but oh well.
Hopefully it would still work even if we switch to UDP

TODO: (serverside)
Every frame:
Attempt to:
1. Get gamestate of all players
2. Send the gamestate of every other player to current player 
'''

import argparse
import logging

from pygame.time import Clock
from ursina import *
from ursina.networking import *

from scripts.server.log_to_variable_handler import LatestLogHandler

#Constants
DATA_RATE = 64 #Times data is sent to the client per second
START_TEXT:str = "The server is not on" #This should never show

#Declare command line arguments
parser = argparse.ArgumentParser(description="The script to start the game server.")
parser.add_argument("-host", "--hostname", type=str, default="localhost", help="The hostname for the server.")
parser.add_argument("-p", "---port", type=int, default=1939, help="The port the server is hosted on.")
args = parser.parse_args()

#Pygame Clock
#There is no way to limit fps in Ursina without a pygame clock as far I as know
clock = Clock()

#Declare Ursina app
app = Ursina(vsync=False)

#Declare server variables
server_peer:RPCPeer = RPCPeer()

#Declare logging
handler = LatestLogHandler()

formatter = logging.Formatter(
    fmt="(%(asctime)s) %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO)
logger:logging.Logger = logging.getLogger(__name__)
logger.addHandler(handler)

#Text displayed
status_text:Text = Text(text=START_TEXT, origin=(-0.5, 0.5), position=(-.5, .5))
count_text:Text = Text(text='', position=(.5, .5))

@rpc(server_peer)
def get_state(connection, time_received, position:int = 42, **kwargs:dict):
    '''
    Receive the gamestate of the connection
    '''
    for k,v in kwargs.items():
        if k == "position":
            logger.debug("position %s gotten!", v)
    logger.info(position)

    #Get events
    #Get player position/velocity

@rpc(server_peer)
def on_connect(connection, time_connected):
    '''
    On connect to server
    '''
    logger.info("%s connected to the server!", connection)

@rpc(server_peer)
def on_disconnect(connection, time_disconnected):
    '''
    On disconnect from server
    '''
    logger.info("%s disconnected from the server!", connection)


def send_state(client:Connection, **kwargs):
    '''
    Sends the gamestate to the client
    '''
    #I think I should only have to send for stuff like camera once?
    #But always send movement info
    #So this should be implemented with like an event system with kwargs probably
    pass

def start_server(hostname, port):
    '''The function that starts the server'''
    logger.info("Starting server on port %d.", port)
    server_peer.start(hostname, port, is_host=True)

def update():
    '''Main handler'''
    server_peer.update()
    if not server_peer.is_running():
        status_text.text = START_TEXT
    else:
        status_text.text = f"latest logs:\n{LatestLogHandler.get_logs()}"
        count_text.text = f"connection count {server_peer.connection_count()}"

def input(key):
    if key == "q":
        logger.warning("Test warning")

if __name__ == "__main__":
    start_server(args.hostname, args.port)
else:
    logger.fatal("Server was not properly run; please run the server directly!.")

while 1:
    #Main loop
    app.step()
    clock.tick(DATA_RATE)

    #This probably should depend on how many players the game is meant for
    #For now I'll assume 2, and just update the code later.
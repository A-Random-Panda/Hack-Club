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
#pylint: disable=pointless-string-statement

import argparse
import logging
from atexit import register
from sys import exit #pylint: disable=redefined-builtin

from pygame.time import Clock
from ursina import *
from ursina.networking import *

from scripts.server.log_to_variable_handler import LatestLogHandler

#Constants
DATA_RATE = 32 #Times data is sent to the client per second
START_TEXT:str = "The server is not on" #This should never show

#Declare command line arguments
parser = argparse.ArgumentParser(description="The script to start the game server.")
parser.add_argument("-host", "--hostname",
                    type=str,
                    default="localhost",
                    help="The hostname for the server.")
parser.add_argument("-p", "--port",
                    type=int,
                    default=1983,
                    help="The port the server is hosted on.")
parser.add_argument("-win", "--window",
                    type=bool,
                    default=True,
                    help="Whether to show a window or not")
args = parser.parse_args()

#Pygame Clock
#There is no way to limit fps in Ursina without a different library as far I as know
clock = Clock()

#Declare Ursina app and properties
#Check window type
if args.window:
    WINDOW_TYPE = 'onscreen'
else:
    WINDOW_TYPE = 'none'

app = Ursina(vsync=False, window_type=WINDOW_TYPE)
#If the screen is showing, disable debug options
if WINDOW_TYPE == "onscreen":
    window.entity_counter.disable()
    window.exit_button.disable()
    window.fps_counter.disable()
    window.collider_counter.disable()

#Declare server variables
in_game:bool  = False
server_peer:RPCPeer = RPCPeer()
connected_ids:list[int] = []

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
status_text:Text = Text(text=START_TEXT, origin=(0, 0), position=(0, 0))
count_text:Text = Text(text='', position=(.5*1.778, .5), origin=(.5, .5))
fps_text:Text = Text(text='', position = (-.5*1.778, .5), origin=(-0.5, 0.5))
a_text:Text = Text(text='', position = (-.5*1.778, -.5), origin=(-0.5, -0.5))

#Information
class ClientInformation():
    '''Information from the client'''
    state_dict = {}

@register
def on_exit() -> None:
    '''Disconnects all on exit'''
    logger.info("Exiting...")
    server_peer.disconnect_all()

@rpc(server_peer)
def test(connection, time_received, your_mom:str):
    '''Testing'''
    a_text.text = (f"Received text: {your_mom} from {id(connection)}")

@rpc(server_peer)
def state_to_server(connection, time_connected, state:str):
    if len(state) > 1460:
        logger.error("Id of %d sent too much data!", id(connection))
        connection.disconnect()
    else:
        ClientInformation.state_dict[id(connection)] = state

@rpc(server_peer)
def on_connect(connection, time_connected):
    '''
    On connect to server
    '''
    #Check how many people are already connected
    if server_peer.connection_count() > 1:
        connection.disconnect()
        logger.info("Client attempted to join a full server")
    else:
        connection_id = id(connection)
        logger.info("Client of id %d connected to the server!", connection_id)
        connected_ids.append(connection_id)

@rpc(server_peer)
def on_disconnect(connection, time_disconnected):
    '''
    On disconnect from server
    '''
    connection_id = id(connection)
    connected_ids.remove(connection_id)
    if connection_id in ClientInformation.state_dict:
        del ClientInformation.state_dict[connection_id]
    logger.info("Client of id %d disconnected from the server!", connection_id)

@rpc(server_peer)
def start_game(connection, time_received):
    '''Function to start the game'''
    if server_peer.connection_count() == 2:
        for i in server_peer.get_connections():
            try:
                server_peer.ingame(i, True)
            except Exception as err:
                logger.error("Caught exception %s, disconnecting peer", err)
                i.disconnect()

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
        #Only runs if the server is running
        #This is where server side verification happens... if it ever gets implemented
        #Doesn't update the text if there's no window
        if WINDOW_TYPE == "onscreen":
            #Update text
            new_status_text = f"latest logs:\n{LatestLogHandler.get_logs()}"
            if status_text.text != new_status_text:
                status_text.text = new_status_text
            new_con_count_text = f"connection count {server_peer.connection_count()}"
            if count_text.text != new_con_count_text:
                count_text.text = new_con_count_text
            #Updates every frame because the fps will be different
            fps_text.text = f"fps: {clock.get_fps()}"

def input(key):# pylint: disable=function-redefined
    '''Input handler'''
    if key == "q":
        logger.warning("Test warning")

if __name__ == "__main__":
    start_server(args.hostname, args.port)
else:
    logger.fatal("Server was not properly run; please run the server directly!.")
    exit(1)

while 1:
    #Main loop
    app.step()# type: ignore
    clock.tick(DATA_RATE)

    #This probably should depend on how many players the game is meant for
    #For now I'll assume 2, and just update the code later.

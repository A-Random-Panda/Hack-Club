'''This file is for testing a multiplayer implementation of Ursina without modifying the main game file'''

#This portion is for what I still need to implement
"""
TODO:
Decide on which method of communication is the best:
1. Sending inputs
2. Sending game state
3. Client authoritive
4. Server authoritive
6. Snapshot Interpolation

The current plan is to just kinda have everything be a server, and running it locally just means hosting it on the computer
"""

import logging
from typing import override

from ursina import *
from ursina.networking import *

#Declare Ursina app
app = Ursina(borderless=False)

#Declare logging
latest_log:str = ""
class LatestLogHandler(logging.NullHandler):
    @override
    def emit(self, record: logging.LogRecord) -> None:
        global latest_log
        latest_log = record.msg

logging.basicConfig(level=logging.INFsO)
logger:logging.Logger = logging.getLogger(__name__)
logger.addHandler(LatestLogHandler())

#Declare server and server variables
server:RPCPeer = RPCPeer()
connection_count:int = 0

#Text displayed
START_TEXT:str = "The server is not on"
status_text:Text = Text(text=START_TEXT, origin=(0, 0))


'''Server class'''
def start_server(hostname, port):
    '''The function that starts the server'''
    logger.info("The server started.")
    server.start(hostname, port, is_host=True)

def update():
    '''Main handler'''
    if not server.is_running():
        status_text.text = START_TEXT
    else:
        status_text.text = f"latest log: {latest_log}"

if __name__ == "__main__":
    logger.info("Ran from main")
    start_server("localhost", 1939)

app.run()


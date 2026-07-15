'''
This file is for testing a multiplayer implementation of Ursina without modifying the main game file
TODO:
Decide on which method of communication is the best:
1. Sending inputs
2. Sending game state
3. Client authoritive
4. Server authoritive
6. Snapshot Interpolation
The current plan is to just kinda have everything be a server, and running it locally just means hosting it on the computer
'''

import argparse
import logging
from typing import override
from collections import deque

from ursina import *
from ursina.networking import *

#Declare command line arguments
parser = argparse.ArgumentParser(description="The script to start the game server.")
parser.add_argument("-host", "--hostname", type=str, default="localhost", help="The hostname for the server.")
parser.add_argument("-p", "---port", type=int, default=1939, help="The port the server is hosted on.")
args = parser.parse_args()

#Declare Ursina app
app = Ursina(borderless=False)

#Declare logging
class LatestLogHandler(logging.Handler):
    '''Handler that puts the latest log into a variable'''
    MAX_LOGS:int = 30
    latest_logs:deque[str] = deque(["Default message"])

    @classmethod
    def save_log(cls, formatted_record: str) -> None:
        '''Saves the log of the message'''
        if len(cls.latest_logs) >= cls.MAX_LOGS:
            cls.latest_logs.popleft()
        cls.latest_logs.append(formatted_record)

    @classmethod
    def get_logs(cls) -> str:
        '''Returns the last MAX_LOGS logs'''
        return "\n".join(cls.latest_logs)

    @override
    def emit(self, record: logging.LogRecord) -> None:
        self.save_log(self.format(record))

handler = LatestLogHandler()

formatter = logging.Formatter(
    fmt="(%(asctime)s) %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO)
logger:logging.Logger = logging.getLogger(__name__)
logger.addHandler(handler)

#Declare server and server variables
server:RPCPeer = RPCPeer()
connection_count:int = 0

#Text displayed
START_TEXT:str = "The server is not on"
status_text:Text = Text(text=START_TEXT, origin=(0, 0))

def start_server(hostname, port):
    '''The function that starts the server'''
    logger.info("Starting server on port %d.", port)
    server.start(hostname, port, is_host=True)

def update():
    '''Main handler'''
    if not server.is_running():
        status_text.text = START_TEXT
    else:
        status_text.text = f"latest logs:\n{LatestLogHandler.get_logs()}"

def input(key):
    if key == "q":
        logger.warning("Test warning")

if __name__ == "__main__":
    start_server(args.hostname, args.port)
    app.run()
else:
    logger.fatal("Server was not properly run; please run the server directly!.")
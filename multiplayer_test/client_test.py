'''This is a dummy client that tests functionality in the server without actual implementation in the main game file.'''

from ursina import *
from ursina.networking import *

app = Ursina()
peer = RPCPeer()

text:Text = Text(text="Client", origin=(-0.5, 0.5), position=(-.5, .5))
count_text:Text = Text(text='', position=(.5, .5))


@rpc(peer)
def on_connect(connection, time_connected):
    '''
    On connect to server
    '''
    print("%s connected to the server!", connection)

@rpc(peer)
def on_disconnect(connection, time_disconnected):
    '''
    On disconnect from server
    '''
    print("%s disconnected from the server!", connection)

@rpc(peer)
def get_state(connection, time_received, position:int ,**kwargs:dict):
    '''
    Receive the gamestate of the connection
    '''
    print(position)

def update():
    '''Main handler'''
    peer.update()
    count_text.text = f"connection count {peer.connection_count()}"

def input(key):
    #connect
    if key == "c":
        print("attempted to connect to server")
        peer.start("localhost", port=1939, is_host=False)
    if key == "h":
        print("attempted get_state call")
        peer.get_state(peer.get_connections()[0], 67, )
app.run()
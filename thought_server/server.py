import argparse
import sys
import time
import socket
import datetime
import threading
import os
from .utils import Connection, Listener
from .thought import Thought
lock = threading.Lock()

METADATA_LENGTH = 20

def handle_connection(connection, dir_path):
    metadata = connection.receive(METADATA_LENGTH)
    thought_length = Thought.thought_length_from_metadata(metadata) 
    thought_bytes = connection.receive(thought_length)
    full_data_bytes = metadata + thought_bytes
    thought = Thought.deserialize(full_data_bytes)

    #TODO: Make path suffix prettier.
    path_suffix = str(obj).replace(' ', '_').replace(':','-') + '.txt'
    user_dir_path = dir_path + "/" + str(userID) + "/"
    
    with lock:
        if not(os.path.exists(user_dir_path) and os.path.isdir(user_dir_path)):
            os.mkdir(user_dir_path)
        file_path = user_dir_path + path_suffix
        with open(file_path, "a+") as f:
            f.write(thought + "\n")
        print(thought)

            
def run_server(address, data_dir):
    address_parsed = address.split(':')
    ip = address_parsed[0]
    port = address_parsed[1]
    listener = Listener(port, ip)
    listener.start()
    while True:
        connection = listener.accept()
        t = threading.Thread(target = handle_connection, args=(connection,data_dir))
        t.start()

if __name__ == '__main__':
    full_address = sys.argv[1]
    obj = datetime.date.fromtimestamp(time.time())
    run_server(full_address,sys.argv[2])


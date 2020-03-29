import argparse
import sys
import time
import socket
import datetime
import threading
import os
import logging
from utils import Connection, Listener
from thought import Thought
import concurrent.futures as cf
import pika

lock = threading.Lock()
THREADS_NUMBER = 5
METADATA_LENGTH = 20



#def handle_connection(connection, dir_path):
#    metadata = connection.receive(METADATA_LENGTH)
#    thought_length = Thought.thought_length_from_metadata(metadata) 
#    thought_bytes = connection.receive(thought_length)
#    full_data_bytes = metadata + thought_bytes
#    thought = Thought.deserialize(full_data_bytes)
#
#    #TODO: Make path suffix prettier.
#    path_suffix = str(obj).replace(' ', '_').replace(':','-') + '.txt'
#    user_dir_path = dir_path + "/" + str(userID) + "/"
#    
#    with lock:
#        if not(os.path.exists(user_dir_path) and os.path.isdir(user_dir_path)):
#            os.mkdir(user_dir_path)
#        file_path = user_dir_path + path_suffix
#        with open(file_path, "a+") as f:
#            f.write(thought + "\n")
#        print(thought)

def handle_connection(connection):
    logging.info('Connection handeled')
    received_bytes = connection.receive(5)
    logging.info('Bytes received')
    recieved = Tought.deserialize(received_bytes)
    print("{data} this was recieved, at this point the server should do its job".format(data=recieved))
    logging.info("Server done job.")
def run_server(host, port, publish):
    logging.info('Server started listening')
    listener = Listener(port, host)
    listener.start()
    executor = cf.ThreadPoolExecutor(THREADS_NUMBER)
    while True:
        connection = listener.accept()
        logging.info('Connection established')
        executor.submit(handle_connection,connection)

#def run_server(address, data_dir):
#    address_parsed = address.split(':')
#    ip = address_parsed[0]
#    port = address_parsed[1]
#    listener = Listener(port, ip)
#    listener.start()
#    while True:
#        connection = listener.accept()
#        t = threading.Thread(target = handle_connection, args=(connection,data_dir))
#        t.start()
#

logging.basicConfig(level = logging.DEBUG, 
                filename = '.logs.txt',
                format = '%(levelname).1s %(asctime)s %(message)s)',
                datefmt = '%Y-%m-%d %H:%M:%S')
if __name__ == '__main__':
    #full_address = sys.argv[1]
    #obj = datetime.date.fromtimestamp(time.time())
    host = sys.argv[1]
    port = sys.argv[2]
    print(host,port,type(host),type(port),"xx")
    dummy = 1
    run_server(host,int(port), dummy)


import time
import math
import sys, socket
import datetime
import logging
import http.client
import requests
#from thought import Thought
#from utils import Connection
#import utils.render as render
logging.basicConfig(level = logging.DEBUG,
                    filename = '.client_logs.txt',
                    format = '%(levelname).1s %(asctime)s %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S')

#def upload_sample(host,port,path):
#    logging.info(f"seinding hen sending client {client_name}")
#    connection = Connection.connect(ip,port)
#    client_name_bytes = str.encode(client_name)
#    connection.send(client_name_bytes)
#    logging.info("Closing client's connection.")
#    connection.close()
def http_upload_thought(host, port, thought):
	url = "http://" + host + ":" + port
	r = requests.get(url, data=thought)

if __name__ == '__main__':
    argv = sys.argv
    #upload_thought(argv[1], int(argv[2]), argv[3])
    http_upload_thought(argv[1],argv[2],argv[3])

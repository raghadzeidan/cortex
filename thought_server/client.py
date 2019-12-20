import time
import math
import sys, socket
import datetime 
from .thought import Thought

def upload_thought(address, user_id, thought):
    ip, port = address
    seconds = int(time.time())
    timestamp_obj = datetime.datetime.fromtimestamp(seconds)
    thought_obj = Thought(user_id, timestamp_obj, thought)
    data = thought_obj.serialize()
    sockt = socket.socket()
    sockt.connect((ip,int(port)))
    sockt.sendall(data)
    sockt.close()

#client.py does not support commandline, TODO: consider returning it
def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        upload_thought(argv[1],argv[2],argv[3])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    import sys
    import socket
    main(sys.argv)

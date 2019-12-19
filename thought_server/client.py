import time
import math
import sys, socket
#this is the client.py of exercise 1, TODO: Update it to match
#thought.py in q2 of exercise 3. its better implemented
#TODO: Solve duplicate code of render_to_bytes and from bytes
def render_to_bytes(user_id, num_bytes):
    user_id_bytearray = bytearray(user_id.to_bytes(num_bytes,sys.byteorder))
    user_id_bytes = bytes(user_id_bytearray)
    return user_id_bytes

def upload_thought(address, user_id, thought):
    address_tuple = tuple(address.split(':'))
    ip, port = address_tuple
    seconds = int(time.time())
    user_id_bytes = render_to_bytes(int(user_id), 8)
    timestamp_bytes = render_to_bytes(seconds, 8)
    thought_length_bytes = render_to_bytes(len(thought),4)
    thought_bytes = str.encode(thought)[::-1]
    data = user_id_bytes + timestamp_bytes + thought_length_bytes + thought_bytes
    sockt = socket.socket()
    sockt.connect((ip,int(port)))
    sockt.sendall(data)
    sockt.close()
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

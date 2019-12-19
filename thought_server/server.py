import argparse
import sys
import time
import socket
import datetime
import threading
import os
lock = threading.Lock()
def bytes_to_long(bytes, flag): #the flag indicates option for an int returned value
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    if flag:
        return int(result)
    return result

def receive_data(address, number_of_bytes):
    count = 0
    data = b''
    while count < number_of_bytes:
        byte = address.recv(1)
        if byte:
            data = data + byte
            count = count + 1
    return data
def handle_connection(client_address, dir_path):
    metadata = receive_data(client_address,20)
    userIDb, time_stampb, thought_sizeb = metadata[0:7][::-1], metadata[8:15][::-1], metadata[16:19][::-1]
    userID = bytes_to_long(userIDb,0)
    time_stamp = bytes_to_long(time_stampb,0)
    thought_size = bytes_to_long(thought_sizeb,1)
    thoughtb = receive_data(client_address, thought_size)[::-1]
    thought =thoughtb.decode('utf-8')
    obj = datetime.datetime.fromtimestamp(time_stamp)
    print_info = f'[{obj}] user {userID}: {thought}'
    path_suffix = str(obj).replace(' ', '_').replace(':','-') + '.txt'
    user_dir_path = dir_path + "/" + str(userID) + "/"
    with lock:
        if not(os.path.exists(user_dir_path) and os.path.isdir(user_dir_path)):
            os.mkdir(user_dir_path)
        file_path = user_dir_path + path_suffix
        with open(file_path, "a+") as f:
            f.write(thought + "\n")
        print(print_info)

            
def run_server(address, data_dir):
    userID = 0
    time_stamp = 0
    thought_size = 0
    address_parsed = address.split(':')
    ip = address_parsed[0]
    port = address_parsed[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,int(port)))
    s.listen(10)
    while True:
        client_address, client_port = s.accept()
        t = threading.Thread(target = handle_connection, args=(client_address,data_dir))
        t.start()

if __name__ == '__main__':
    full_address = sys.argv[1]
    obj = datetime.date.fromtimestamp(time.time())
    run_server(full_address,sys.argv[2])


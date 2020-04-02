from cortex_pb2 import 	User, Snapshot
import time, sys
import gzip
#from reader import read_info
INT_SIZE = 4
TIMESTAMP_SIZE = 8

def read_user_information(fd):
	'''receives file descriptor, and reads user information from it
	wraps it in a User object that was extracted
	from .protobuf file'''
	
	length_byte = fd.read(INT_SIZE)
	user_info_length = int.from_bytes(length_byte, byteorder='little')
	user_bytes_string = fd.read(user_info_length)
	user = User()
	user.ParseFromString(user_bytes_string)
	return user
	
	
def read_shit():
	path = "/home/user/Desktop/sample.mind.gz"
	fd = gzip.open(path, "rb")
	
	l = fd.read(INT_SIZE)
	print(l)
	u_l = int.from_bytes(l, byteorder='little')
	user_bytes_string = fd.read(u_l)
	user = User()
	user.ParseFromString(user_bytes_string)
	print(user)
	print(type(user.gender))
	
	
	new_length = fd.read(INT_SIZE)
	print(new_length)
	new_length_as_int = int.from_bytes(new_length, byteorder='little')
	print(new_length_as_int)
	snapshot = Snapshot()
	bts = fd.read(new_length_as_int)
	snapshot.ParseFromString(bts)
	print(snapshot)
	new_new_length = fd.read(INT_SIZE)
	new_new_length_as_int = int.from_bytes(new_new_length, byteorder='little')
	print (new_new_length_as_int)
	snapshot = Snapshot()
	bts = fd.read(new_new_length_as_int)
	snapshot.ParseFromString(bts)
	print(snapshot)
	print("x", snapshot.feelings)
	print(snapshot.datetime)
	print(snapshot.color_image)
	
def read_empty_shit():
	path = "/home/user/Desktop/lol.txt"
	fd = open(path, "r")
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))

	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	x = fd.read(1)
	print(x)
	print(type(x))
	print(x == b'')
	
#def hello_worker_callback(channel, method, properties, body):
#    print(f"hello worker has started, with {body}")

#channel.queue_declare(queue = 'hello_queue')
#channel.basic_consume(queue = 'hello_queue', auto_ack = True, on_message_callback = hello_worker_callback)
#channel.start_consuming()

#read_shit()
#read_empty_shit()

s= {'translate', 'color_image'}
s.add('pose')
ss = '@'.join(s)
print(ss)


from .parsers_main import subscribe
import numpy as np
import matplotlib.pyplot as plt
import pika
from ..mq import MQer
import json
import blessings
term = blessings.Terminal()


@subscribe('depth_image')
def parse_that_fucking_depth(data):
	print(term.red_on_white(str(data)))
	dic = json.loads(data)
	publish_depth = {}
	publish_depth['user'] = dic['user']
	publish_depth['datetime'] = dic['datetime']
	
	depth_path = dic['depth_image']['data_path']
	height = dic['depth_image']['height']
	width = dic['depth_image']['width']
	float_array = np.load(depth_path)
	plt.imshow(float_array, cmap='hot', interpolation='nearest')
	user_id = dic['user']['userId']
	datetime = dic['datetime']
	save_path = f'/home/user/Desktop/volume/depth_images/images/{user_id}_{datetime}.png'
	publish_depth['depth_image'] = save_path
	plt.savefig(save_path)
	return json.dumps(publish_depth)

def depth_image_parser_callback(channel, method, properties, body):
	'''a callback for the parsing feelings function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	#extracting from user+snapshot (just like run_parser)
	#consider making them one code
	#extracting..
	to_publish=parse_that_fucking_depth(body)
	channel.exchange_declare('depth_image', exchange_type='fanout')
	channel.basic_publish(exchange='depth_image', routing_key='', body=to_publish)


def depth_image_parser_main(mq_url):#Consider the initialization to be one-for-all
	print(mq_url)
	mq = MQer(mq_url)
	mq.create_exchange('parsers', exchange_type = 'fanout')
	queue_name = mq.subscribe_to_exchange('parsers', return_queue = True) #we have a new queue connected to the exchange
	mq.connect_to_consume_function(queue_name, callback_function=depth_image_parser_callback)
	print('depth consuming...')
	mq.start_consuming()
	

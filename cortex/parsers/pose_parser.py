from .parsers_main import subscribe
from ..mq import MQer
import pika
import json
import blessings
term = blessings.Terminal()


@subscribe('pose')
def parse_that_fucking_pose(data):
	'''parser receives raw data that is consumed from MQ (json format of User+snapshot)
	parses pose data and sticks userdata with them and republishes to his exchange '''
	dic = json.loads(data)
	publish_pose = {}
	publish_pose['user'] = dic['user']
	publish_pose['datetime'] = dic['datetime']
	publish_pose['pose'] = dic['pose']
	debug = json.dumps(publish_pose)
	return debug

    
def pose_parser_callback(channel, method, properties, body):
	'''a callback for the parsing pose function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	print(term.blue_on_white("Pose parsing function triggered."))
	to_publish = parse_that_fucking_pose(body)
	print(term.blue_on_white("Pose processed and republishing to message queue"))
	channel.exchange_declare('pose', exchange_type='fanout')
	channel.basic_publish(exchange='pose', routing_key='', body=to_publish)
    
    

def pose_parser_main(mq_url):
	mq = MQer(mq_url)
	mq.create_exchange('parsers', exchange_type = 'fanout')
	queue_name = mq.subscribe_to_exchange('parsers', return_queue = True) #we have a new queue connected to the exchange
	mq.connect_to_consume_function(queue_name, callback_function=pose_parser_callback)
	print(f'pose consuming from {mq_url}...')
	mq.start_consuming()

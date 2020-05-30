from .parsers_main import subscribe
import pika
from ..mq import MQer
import json
import blessings
term = blessings.Terminal()

@subscribe('feelings')
def parse_those_fucking_feelings(data):
	dic = json.loads(data)
	publish_feelings = {}
	publish_feelings['user'] = dic['user']
	publish_feelings['datetime'] = dic['datetime']
	publish_feelings['feelings'] = dic['feelings']
	debug = json.dumps(publish_feelings)
	return debug
	
    
def feelings_parser_callback(channel, method, properties, body):
	'''a rabbitMQ callback function '''
	print(term.blue_on_white("Feelings parsing function triggered."))
	to_publish = parse_those_fucking_feelings(body)
	print(term.blue_on_white("Feelings processed and republishing to message queue"))
	channel.exchange_declare('feelings', exchange_type='fanout')
	channel.basic_publish(exchange='feelings', routing_key='', body=to_publish)


def feelings_parser_main(mq_url):
	mq = MQer(mq_url)
	mq.create_exchange('parsers', exchange_type = 'fanout')
	queue_name = mq.subscribe_to_exchange('parsers', return_queue = True) #we have a new queue connected to the exchange
	mq.connect_to_consume_function(queue_name, callback_function=feelings_parser_callback)
	print(f'feelings consuming from {mq_url}...')
	mq.start_consuming()


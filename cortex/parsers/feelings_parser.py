from .parsers_main import subscribe
import pika
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
	return json.dumps(publish_feelings)
	
    
def feelings_parser_callback(channel, method, properties, body):
	'''a callback for the parsing feelings function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	
	to_publish = parse_those_fucking_feelings(body)
	channel.exchange_declare('feelings', exchange_type='fanout')
	channel.basic_publish(exchange='feelings', routing_key='', body=to_publish)

    
    
#print('Feelings parser consuming...')
def feelings_parser_main(mq):
	#MQ related to localhost
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare('parsers', exchange_type='fanout')

	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange = 'parsers', queue = queue_name)
	print('feelings consuming...')
	channel.basic_consume(queue=queue_name, on_message_callback=feelings_parser_callback, auto_ack=True)
	channel.start_consuming()

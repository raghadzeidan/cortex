from .parsers_main import subscribe
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
	return json.dumps(publish_pose)

    
def pose_parser_callback(channel, method, properties, body):
	'''a callback for the parsing pose function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	#received user+snapshot in json format
	#parsing to get user+pose_information in json format
	to_publish = parse_that_fucking_pose(body)
	
	#republishing in designated exchange for other consumers(saver)
	channel.exchange_declare('pose', exchange_type='fanout')
	channel.basic_publish(exchange='pose', routing_key='', body=to_publish)
    
    

def pose_parser_main(mq):
	#MQ related to localhost
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare('parsers', exchange_type='fanout')

	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange = 'parsers', queue = queue_name)
	print('pose consuming...')
	channel.basic_consume(queue=queue_name, on_message_callback=pose_parser_callback, auto_ack=True)
	channel.start_consuming()

from .parsers_main import subscribe
import pika
import json
import blessings
term = blessings.Terminal()


@subscribe('color_image')
def parse_that_fucking_image(data):
    print(term.cyan(f'PARSER 1 RECIEVED: {data}'))

def color_image_parser_callback(channel, method, properties, body):
	'''a callback for the parsing feelings function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	#extracting from user+snapshot (just like run_parser)
	#consider making them one code
	#extracting..
	dic = json.loads(body)
	with open('/home/user/Desktop/volume/color_img.txt','w') as f:
		f.write(str(dic['color_image']) + '\n')
	parse_that_fucking_image(dic['color_image'])

def color_image_parser_main(mq):#Consider the initialization to be one-for-all
	print(mq)
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.exchange_declare('parsers', exchange_type='fanout')
	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange = 'parsers', queue = queue_name)
	print('color_Image parser consuming...')

	channel.basic_consume(queue=queue_name, on_message_callback=color_image_parser_callback, auto_ack=True)
	channel.start_consuming()
	

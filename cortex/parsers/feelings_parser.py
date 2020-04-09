from .parsers_main import subscribe
import pika
import json
import blessings
term = blessings.Terminal()

@subscribe('feelings')
def parse_those_fucking_feelings(data):
	'''(should, needs extracting)receives user+relevant feelings (json) snapshot and works on feelings part '''
	print(term.red(f'FEELINGS PARSER RECIEVED: \n'))
	print(term.red_on_black(str(data)))
    
def feelings_parser_callback(channel, method, properties, body):
	'''a callback for the parsing feelings function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	#extracting from user+snapshot (just like run_parser)
	#consider making them one code
	#extracting..
	dic = json.loads(body)
	with open('/home/user/Desktop/volume/feelings_input.txt','w') as f:
		f.write(str(dic['feelings']) + '\n')
	parse_those_fucking_feelings(dic['feelings'])
	
    
    
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

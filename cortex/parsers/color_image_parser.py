from .parsers_main import subscribe
import pika
import time
from PIL import Image
import json
from ..mq import MQer
import blessings
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
term = blessings.Terminal()


@subscribe('color_image')
def parse_that_fucking_image(data):
	print(term.red_on_white(str(data)))
	dic = json.loads(data)
	print(term.red_on_white(str(dic)))
	color_image_publish = {}
	color_image_publish['user'] = dic['user']
	color_image_publish['datetime'] = dic['datetime']
	#processing of color_image
	image_bytes_path = dic['color_image']['data_path']
	width, height = dic['color_image']['width'], dic['color_image']['height']
	with open(image_bytes_path, 'rb') as f:
		print(term.green_on_black(f'Opened path {image_bytes_path}'))
		image_bytes = f.read()
	print(term.green_on_black(f'width:{width} - heigh:{height}'))
	print(term.green_on_black(f'type: {type(image_bytes)}, length: {len(image_bytes)}'))
	image = Image.frombytes('RGB', (width, height), (image_bytes))
	#image.putdata(image_bytes)
	user_id = dic['user']['userId']
	datetime = dic['datetime']
	save_path = f'/home/user/Desktop/volume/color_images/images/{user_id}_{datetime}.png'
	image.save(save_path)
	imgplot = plt.imshow(mpimg.imread(save_path))
	#plt.show()
	time.sleep(0.2)
	plt.close()
	print(term.green_on_black(f'Saved image on path {save_path}'))
	color_image_publish['color_image'] = save_path
	return json.dumps(color_image_publish)
		
    

def color_image_parser_callback(channel, method, properties, body):
	'''a callback for the parsing feelings function.
	PROJECT: this allows decoupiling between MQ and actual parsing function'''
	
	to_publish=parse_that_fucking_image(body)
	channel.exchange_declare('color_image', exchange_type='fanout')
	channel.basic_publish(exchange='color_image', routing_key='', body=to_publish)

def color_image_parser_main(mq_url):#Consider the initialization to be one-for-all
	print(mq_url)
	
	mq = MQer(mq_url)
	
	mq.create_exchange('parsers', exchange_type = 'fanout')
	queue_name = mq.subscribe_to_exchange('parsers', return_queue = True) #we have a new queue connected to the exchange
	mq.connect_to_consume_function(queue_name, callback_function=color_image_parser_callback)
	print('parser_consuming consuming...')
	mq.start_consuming()
	
	#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	#channel = connection.channel()
	#channel.exchange_declare('parsers', exchange_type='fanout')
	#result = channel.queue_declare(queue='', exclusive=True)
	#queue_name = result.method.queue
	#channel.queue_bind(exchange = 'parsers', queue = queue_name)
	#print('color_Image parser consuming...')

	#channel.basic_consume(queue=queue_name, on_message_callback=color_image_parser_callback, auto_ack=True)
	#channel.start_consuming()
	

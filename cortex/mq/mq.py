from furl import furl
import pika


def find_mqdriver(furl_object):
	mq = furl_object.scheme
	if mq in MQ_DRIVERS:
		return mq
	logging.error('invalud MQ URL - MQer')
	raise TypeError(f'Unsupported message queue: {mq}')
	
class RabbitDriver():
	'''This is our supported MQ, rabbit MQ driver.
	the way this infrastructure works is similiar to readers.
	drivers have to implement: create_exchange, publish, consume etc...
	chose relatively general names, for potential logic in MQer '''
	
	def __init__(self, host, port):
		params = pika.ConnectionParameters(host,port)
		self.connection = pika.BlockingConnection(params)
		self.channel = self.connection.channel()
		
	def create_exchange(self, exchange_name, exchange_t):
		self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_t)
		
	def publish(self, ex, key, bod):
		self.channel.basic_publish(exchange=ex, routing_key=key, body=bod)
	
	def create_queue(self, q_name, exclussive):
		return self.channel.queue_declare(queue=q_name, exclusive=exclussive)
		
	def subscribe_to_exchange(self, exchange_name, q_name=''):
		result = self.create_queue(q_name, True)
		qresult_name = result.method.queue
		self.channel.queue_bind(exchange = exchange_name, queue = qresult_name)
		return qresult_name
		
	def connect_to_function(self, q_name, callback_func, auto_ackk):
		self.channel.basic_consume(queue=q_name, on_message_callback=callback_func, auto_ack=auto_ackk)
		
	def start_consuming(self):
		self.channel.start_consuming()
		
	def should_return(self, function):
		'''this function implies wether we should return a value or not in this specific mq implementation
		this is used when two different MQ operations are related to one  another
		like subscribe_to_change and start_consuming'''
		if function == 'subscribe_to_exchange':
			return True
		return False
		
		
	
	
MQ_DRIVERS = {'rabbitmq': RabbitDriver}

class MQer:
	
	
	def __init__(self, url):
		ffurl = furl(url)
		port = ffurl.port
		host = ffurl.host
		driver_name = find_mqdriver(ffurl)
		MQDriver = MQ_DRIVERS[driver_name]
		self.driver = MQDriver(host,port)
        
	
	def subscribe_to_exchange(self, exchange_name, queue_name='', return_queue=False):
		queue_name = self.driver.subscribe_to_exchange(exchange_name, queue_name)
		if return_queue:
			return queue_name
			
	def create_exchange(self, exchange, exchange_type):
		self.driver.create_exchange(exchange, exchange_type)
			
	def publish(self, exchange, key, body):
		self.driver.publish(exchange, key, body)
	
	def create_queue(self, queue_name, exc=True):
		self.driver.create_queue(queue_name, exc)
		
	def connect_to_consume_function(self, queue_name, callback_function, auto_ack = True):
		self.driver.connect_to_function(queue_name, callback_function, auto_ack)
	
	def start_consuming(self):
		self.driver.start_consuming()
		
	
		
		
	
		

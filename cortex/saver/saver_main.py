from .saver import DatabaseDriver, DB_SUPPORTED_FORMATS
from ..mq import MQer
saver = None
def main_saver_callback(channel, method, properties, body):
	'''every parser sticked his information in his dictionary under the
	key of his name, which is also the name of the exchange he publishes at'''
	if not saver:
		raise ValueError('Something went wrong, save uninitiolized')
	data_format = method.exchange
	if data_format not in DB_SUPPORTED_FORMATS:
		raise ValueError(f'Recieved information of unsupported format {data_format}')
	saver.save(data_format, body) 

def run_saver_as_microservice(db_url, mq_url):
	global saver
	saver = DatabaseDriver(db_url)
	mq = MQer(mq_url)
	
	for formaat in DB_SUPPORTED_FORMATS: #iterating over supported saving-formats and connecting them to his callback function
		mq.create_exchange(formaat, exchange_type = 'fanout')
		queue_name = mq.subscribe_to_exchange(formaat, return_queue = True)
		mq.connect_to_consume_function(queue_name, callback_function=main_saver_callback)
	mq.start_consuming()
	
	

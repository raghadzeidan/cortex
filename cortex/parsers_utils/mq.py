import pika
print("mq_initialized")

params = pika.ConnectionParameters('localhost')
mainQ_connection = pika.BlockingConnection(params)


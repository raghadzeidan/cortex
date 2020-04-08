import pika
import logging

params = pika.ConnectionParameters()
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

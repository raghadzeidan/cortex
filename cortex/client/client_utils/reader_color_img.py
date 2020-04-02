#from PIL import Image
import logging
#from ..utils import read_data
from mq import channel
#def parse_color_img(snapshot):
#    #TODO:processing this data from the snapshot
#    image_height = read_bytes(INT_SIZE, return_as=int)
#    image_width = read_bytes(INT_SIZE, return_as=int)
#    BGR_values = read_bytes(BGR_SIZE*image_width*image_height) #returns as bytes
#    BGR_values_barray = bytearray(BGR_values)
#    color_img = Image.new('RGB',(image_width, image_height), color='white')
#    color_pix = color_img.load()
#    for i in range(0,image_width*image_height, image_height):
#        for j in range(0,image_width,BGR_SIZE):
#            R, G, B = BGR_values_barray[i+j+2, i+j+1, i+j]
#            pix[i,j] = (R, G, B)

logging.basicConfig(level = logging.DEBUG, 
                filename = '.logs.txt',
                format = '%(levelname).1s %(asctime)s %(message)s)',
                datefmt = '%Y-%m-%d %H:%M:%S')

def color_worker_callback(channel, method, properties, body):
    print(f'color worked has started, with {body}')

channel.queue_declare(queue='color_queue')
channel.basic_consume(queue = 'color_queue', auto_ack = True, on_message_callback = color_worker_callback)
channel.start_consuming()

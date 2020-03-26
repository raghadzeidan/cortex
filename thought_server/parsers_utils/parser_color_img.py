from PIL import Image
from ..utils import read_data

def parse_color_img(snapshot):
    #TODO:processing this data from the snapshot
    image_height = read_bytes(INT_SIZE, return_as=int)
    image_width = read_bytes(INT_SIZE, return_as=int)
    BGR_values = read_bytes(BGR_SIZE*image_width*image_height) #returns as bytes
    BGR_values_barray = bytearray(BGR_values)
    color_img = Image.new('RGB',(image_width, image_height), color='white')
    color_pix = color_img.load()
    for i in range(0,image_width*image_height, image_height):
        for j in range(0,image_width,BGR_SIZE):
            R, G, B = BGR_values_barray[i+j+2, i+j+1, i+j]
            pix[i,j] = (R, G, B)


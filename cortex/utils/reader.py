from .thought import render_from_bytes
from PIL import Image
from ..thought_server.parsers_utils import parser_hello
from ..utils import read_bytes
import datetime as dt
USER_ID_SIZE = 8
TIMESTAMP_SIZE = 8
INT_SIZE = 4
CHAR_SIZE = 1
COORDINATE_SIZE = 8
BGR_SIZE = 3
FLOAT_SIZE = 4



class Reader:
    def read_info(data_size,return_as=None):
        data = self.fd.read(data_size)
        if return_as:
            return render_from_bytes(data) if return_as==int else data.decode('utf-8')
        return data
    def open_file(self):
        self.fd = open(self.path,"rb")
    def close_file(self):
        self.fd.close()
    def __init__(self, path):
        self.path = path
        self.init_metadata()
    def init_metadata(self):
        self.open_file()
        self.hello = parse_hello(self.fd)
        self.user_id = self.hello.user_id
        self.username = self.hello.username
        self.birthday = self.hello.birthdate
        self.gender = self.hello.gender
        self.close_file()
    def __iter__(self):
        self.open_file()
        
        timestamp_ms = read_bytes(TIMESTAMP_SIZE, return_as=int)
        timestamp = int((timestamp_ms/1000)%60)
        
        position_x = read_bytes(COORDINATE_SIZE, return_as=int)
        position_y = read_bytes(COORDINATE_SIZE, return_as=int)
        position_z = read_bytes(COORDINATE_SIZE, return_as=int)
        

        head_pose_x = read_bytes(COORDINATE_SIZE, return_as=int)
        head_pose_y = read_bytes(COORDINATE_SIZE, return_as=int)
        head_pose_z = read_bytes(COORDINATE_SIZE, return_as=int)
        head_pose_w = read_bytes(COORDINATE_SIZE, return_as=int)
        
        #TODO: self.render_color_image() and fix processing
        image_height = read_bytes(INT_SIZE, return_as=int)
        image_width = read_bytes(INT_SIZE, return_as=int)
        RGB_values = read_bytes(BGR_SIZE*image_width*image_height) #returns as bytes
        #TODO: parse_color_img()
        
        #TODO: self.render_depth_image() and fix processing after more info
        depth_height = read_bytes(INT_SIZE, return_as=int)
        depth_width = read_bytes(INT_SIZE, return_as=int)
        depth_values = read_bytes(FLOAT_SIZE*depth_height*depth_width) #returns as bytes
        depth_values_barray = bytearray(depth_values)
        depth_img = Image.new('f',(depth_width,depth_height))
        depth_pix = depth_img.load()
        for i in range(0,depth_height*depth_width, depth_height):
            for j in range(0,image_width, FLOAT_SIZE):
                float_chunk[i+j:i+j+4]
                depth_pix[i,i+j]

        hunger_feeling = read_bytes(FLOAT_SIZE, return_as=int)
        thirst_feeling = read_bytes(FLOAT_SIZE, return_as=int)
        exh_feeling = read_bytes(FLOAT_SIZE, return_as=int)
        happy_feeling = read_bytes(FLOAT_SIZE, return_as=int)
        
        feelings = (hunger_feeling, thirst_feeling, exh_feeling, happy_feeling)
        translation = (position_x, position_y, position_z)
        rotation = (head_pose_x, head_pose_y, head_pose_z, head_pose_w)

        return Snapshot(timestamp, translation, rotation, color_img, depth_impg, feelings)


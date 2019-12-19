import datetime
import sys

def render_from_bytes(byytes):
    result = 0
    for b in byytes:
        result = result * 256 + int(b)
    return result

def render_to_bytes(string, num_bytes):
    barray = bytearray(string.to_bytes(num_bytes, sys.byteorder))
    bbytes = bytes(barray)
    return bbytes
class Thought:  
    def __init__(self, user_id,time, thought):
        self.user_id = user_id
        self.thought = thought
        self.timestamp = time
    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'
    def __str__(self):
        return f'[{str(self.timestamp)}] user {self.user_id}: {self.thought}'
    def __eq__(self, other):
        if not(isinstance(self, Thought) and isinstance(other, Thought)):
            return False
        return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought
    def serialize(self):
        user_bytes = render_to_bytes(self.user_id, 8)
        time_bytes = render_to_bytes(int(self.timestamp.timestamp()), 8)
        length_bytes = render_to_bytes(len(self.thought), 4)
        thought_bytes = str.encode(self.thought)
        data = user_bytes + time_bytes + length_bytes + thought_bytes
        return data

    @staticmethod
    def deserialize( data):
        userb, timeb, lengthb = data[0:8][::-1], data[8:16][::-1], data[16:20][::-1]
        thoughtb = data[20:][::-1]
        time_stamp = render_from_bytes(timeb)
        lengthh = render_from_bytes(lengthb)
        user = render_from_bytes(userb)
        thought = thoughtb.decode('utf-8')
        thought = thought[::-1]
        return Thought(user, datetime.datetime.fromtimestamp(time_stamp), thought)
        

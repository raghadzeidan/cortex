from ..utils import Hello, read_data

def parse_hello(fd):
    '''receives a file descritor, and parses the metadata from it
    and puts it into the Hello class and returns it'''
    user_id = read_bytes(USER_ID_SIZE, return_as=int)
    name_length = read_bytes(INT_SIZE, return_as=int)
        
    #next chuck of metadata has: name_length bytes, 4 birthdate
    #bytes, 1 gender byte
    metadata_bytes = read_bytes(name_length + INT_SIZE + CHAR_SIZE)
    name = read_bytes(name_length, return_as=str)
    
    birthdate_timestamp = read_bytes(INT_SIZE, return_as=int)
    birthday = dt.datetime.fromtimestamp(birthdate_timestamp)
    gender = read_bytes(CHAR_SIZE, return_as=str)
    return Hello(user_id, user_name, birthdate, gender)

import socket
class Connection:
    def __init__(self, soc):
        self.socket = soc
    def __repr__(self):
        peer = self.socket.getpeername()
        temp_sock = self.socket.getsockname()
        return f'<Connection from {temp_sock[0]}:{temp_sock[1]} to {peer[0]}:{peer[1]}>'
    def send(self, data):
        self.socket.sendall(data)
    def receive(self, size):
        count = 0
        data = b''
        while count < size:
            byte = self.socket.recv(1)
            if byte:
                data = data+byte
                count = count + 1
            else:
                raise Exception
        return data
    def close(self):
        self.socket.close()
    def __enter__(self):
        return self
    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        '''this class method opens a socket to the specifide host and port,
            and returns a Connection object'''
        s = socket.socket()
        s.connect((host,port))
        return Connection(s)

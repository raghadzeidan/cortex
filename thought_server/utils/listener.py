from .connection import Connection
import socket

class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host!r}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'
    def start(self):
        if self.reuseaddr == True:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host, self.port))
        self.s.listen(self.backlog)
        self.active_connections = 0
    def stop(self):
        self.active_connections = 0
        self.s.close()
    def accept(self):
        client_address, client_port = self.s.accept()
        self.active_connections = self.active_connections + 1
        return Connection(client_address)
    def __enter__(self):
        self.start()
        return self
    def __exit__(self, x,y,z):
        self.stop()

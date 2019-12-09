import socket
import queue
from arduino_firmata import Arduino

class TcpClient(object):

    def __init__(self, sockfd: socket.socket, address: (str, int), arduino_service:Arduino):
        print("HERE")
        self.arduino=arduino_service
        self.sockfd = sockfd
        self.address = address
        self.message_fragment = b''
    
    def recv_tcp_fragment(self, tcpmsg: bytes):
        if bytes(";", 'ascii') in tcpmsg:
            index = tcpmsg.find(bytes(';', 'ascii'))
            message = self.message_fragment+tcpmsg[0:index]
            self.message_fragment = tcpmsg[index+1:]
            self.on_message(message)
        else:
            self.message_fragment += tcpmsg

    def on_message(self, message: str):
        print(message)

    def close(self):
        self.sockfd.close()


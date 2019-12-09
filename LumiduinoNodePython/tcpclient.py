import socket
import queue
from LumiduinoNodePython.arduino_firmata import FirmataArduino
from LumiduinoNodePython.model.tcpmessage import BaseMessage, LumiduinoOpcodes, baseMessageParser
from LumiduinoNodePython.customlogger import CustomLogger

class TcpClient(object):

    def __init__(self, sockfd: socket.socket, address: (str, int),
     arduino_service:FirmataArduino, logger: CustomLogger):
        self.logger = logger
        self.arduino=arduino_service
        self.sockfd = sockfd
        self.address = address
        self.message_fragment = b''
    
    def recv_tcp_fragment(self, tcpmsg: bytes):
        if bytes(";", 'ascii') in tcpmsg:
            index = tcpmsg.find(bytes(';', 'ascii'))
            self.last_message = self.message_fragment+tcpmsg[0:index]
            self.message_fragment = tcpmsg[index+1:]
            self.on_message(self.last_message)
        else:
            self.message_fragment += tcpmsg

    def on_message(self, message: bytes):
        parsed_message = baseMessageParser.parse_message(message)
        switch = {
            LumiduinoOpcodes.ADDSTRIP.value: self.arduino.register_strip,
            LumiduinoOpcodes.SETPIXELVALUE.value: self.arduino.send_pixelval,
            LumiduinoOpcodes.SHOWSTRIP.value: self.arduino.show_strip 
        }
        function = switch.get(parsed_message.opcode,
            lambda *args: self.on_unknown_opcode(parsed_message.opcode, parsed_message.args))
        function(*parsed_message.args)

    def on_unknown_opcode(self, opcode, args):
        self.logger.log_warning("Unknown message recieved: {}, {}".format(opcode, args))

    def close(self):
        self.sockfd.close()


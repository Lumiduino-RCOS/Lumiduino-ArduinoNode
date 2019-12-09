from enum import Enum
import struct

class LumiduinoOpcodes(Enum):
    ADDSTRIP=1
    SETPIXELVALUE=2
    SHOWSTRIP=3
    UNKNOWN=100

class BaseMessage(object):
    opcode:int
    args: list

class baseMessageParser(object):

    @staticmethod
    def parse_message(message: bytes) -> BaseMessage:
        message_split = message.decode('ascii').split(',')
        message_parsed = BaseMessage()
        message_parsed.opcode = int(message_split[0])
        message_parsed.args = message_split[1:]
        for i, value in enumerate(message_parsed.args):
            message_parsed.args[i] = int(value)
        return message_parsed
        


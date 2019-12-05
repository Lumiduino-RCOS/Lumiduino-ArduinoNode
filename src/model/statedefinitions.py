from enum import Enum

class ArduinoState(Enum):
    STARTUP = 0
    CONNECTED = 1
    ERROR = 2
'''from arduino_firmata import FirmataArduino
from tcpserver import TcpServer'''
import time
from LumiduinoNodePython.containers import LumiduinoServer
import signal
"""nar = FirmataArduino('/dev/ttyACM0')
nar.register_strip(9, 100)
while True:
    for i in range(100):
        nar.send_pixelval(i, 100, 100, 100)
        nar.show_strip()
    nar.show_strip()
    time.sleep(1)
    for i in range(100):
        nar.send_pixelval(i, 0,0,0)
        nar.show_strip()
    nar.show_strip()"""

def safely_close(signalnumber, frame):
    LumiduinoServer.logger().log_task_start("Beginning safe close sequence")
    LumiduinoServer.broadcaster().close()
    LumiduinoServer.lumiduino_tcp_server().close()
    LumiduinoServer.arduino_service().close()
    LumiduinoServer.logger().close()
    exit(0)

LumiduinoServer.config.override({
    "logging": {
        'verbose': True,
        "file_path": "."
    },
    "arduino": {
        'location': "/dev/ttyACM0"
    },
    "server": {
        "port": 6879
    }
})
broadcaster = LumiduinoServer.broadcaster()
arduino = LumiduinoServer.arduino_service()
server = LumiduinoServer.lumiduino_tcp_server()

signal.signal(signal.SIGTERM, safely_close)
signal.signal(signal.SIGINT, safely_close)

#tpserve = TcpServer(6879)
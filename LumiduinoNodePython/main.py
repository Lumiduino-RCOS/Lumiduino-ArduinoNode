'''from arduino_firmata import FirmataArduino
from tcpserver import TcpServer'''
import time
from containers import LumiduinoServer
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
server = LumiduinoServer.lumiduino_tcp_server()
#tpserve = TcpServer(6879)
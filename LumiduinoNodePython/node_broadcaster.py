import socket
from concurrent.futures import ThreadPoolExecutor
import simplejson
import time
from LumiduinoNodePython.customlogger import CustomLogger
from LumiduinoNodePython.arduino_firmata import FirmataArduino
from threading import Thread
class NodeInformationBroadcaster(object):

    def __init__(self, serverport, logger: CustomLogger, arduino: FirmataArduino):
        self.logger = logger
        self.logger.log_task_start("Information Broadcaster")
        self.arduino = arduino      
        self.running = True 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.message = {
           "address": self.get_address_name(),
           "port": serverport,
           "arduino_lights": arduino.strip
        }
        self.logger.log_activity("message is {}".format(self.message))
        self.broadcast_loop = Thread(target=self.threaded_broadcast_loop)
        self.broadcast_loop.start()

    def get_address_name(self):
        hostname = socket.gethostname()
        address = socket.gethostbyname(hostname)
        return address

    def threaded_broadcast_loop(self):
        while self.running:
            if self.arduino.strip:
                #print(self.arduino.strip.pixel_array)
                self.message['arduino_lights'] = simplejson.dumps(self.arduino.strip, for_json=True)
            message = simplejson.dumps(self.message)
            self.socket.sendto(message.encode('ascii'), ('<broadcast>',2050))
            time.sleep(1)

    def close(self):
        self.running = False
        self.logger.log_task_start("Close Broadcast Loop")
        self.broadcast_loop.join()
        self.logger.log_task_stop("Close Broadcast Loop")
        
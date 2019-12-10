from pyfirmata import Arduino, util
import time
import threading
import queue
import concurrent.futures
from LumiduinoNodePython.customlogger import CustomLogger
from LumiduinoNodePython.model.lightstrip import NeopixelStrip
import LumiduinoNodePython.model.firmataproto as proto
NEOPIXEL_SET = 0x72
NEOPIXEL_REGISTER = 0x74
NEOPIXEL_SHOW = 0x80

class FirmataArduino(object):

    def __init__(self, port, logger:CustomLogger):
        # initial state is board is not connected
        self.port = port
        self.logger = logger
        self.send_queue = queue.Queue(maxsize=30)
        self.board: Arduino = None
        self.strip: NeopixelStrip = None

        self.running = True
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.recv_future: concurrent.futures.Future = None
        self.send_future: concurrent.futures.Future = None
        
        future = self.executor.submit(self.connect_board, 115200)
        future.add_done_callback(self.start_listening)

    def connect_board(self, baudrate: int):
        start_time = time.time()
        self.logger.log_task_start("Connecting arduino at {}".format(self.port))
        self.board = Arduino(self.port, baudrate=baudrate)
        end_time = time.time()
        time_took = end_time-start_time
        self.logger.log_task_stop("Arduino at {} has been connected in {} seconds".format(self.board.name, time_took))

    def start_listening(self, from_future):
        self.recv_future = self.executor.submit(self.recv_thread)
        self.send_future = self.executor.submit(self.send_thread)

    def recv_thread(self):
        self.logger.log_task_start("Starting recv processing for arduino")
        while self.running:
            time.sleep(1)
        self.logger.log_task_stop("Stopping recv processing for arduino")

    def send_thread(self):
        """ Firmata will error if commands are sent too quickly"""
        self.logger.log_task_start("Starting send queue processing for arduino")
        while self.running:
            try:
                (command, args) = self.send_queue.get(timeout=1)
                self.board.send_sysex(command, args)
                time.sleep(.004)
            except queue.Empty:
                continue
        self.logger.log_task_stop("Stopping send queue processing for arduino")
    
    def add_send(self, command: bytes, args: list):
        self.send_queue.put((command, args))

    def register_strip(self, pin: int, count: int):
        self.add_send(proto.REGISTER_NEOPIXEL, [pin, count])
        #self.board.send_sysex(0x74, [pin, count])
        self.logger.log_activity('registered new strip on pin {} with lenght {}'.format(pin, count))
        self.strip = NeopixelStrip(count)

    def send_pixelval(self, pixel, r, g, b):
        if self.strip.change_pixel_value(pixel, r, g, b):
            self.add_send(proto.SET_NEOPIXEL, [pixel, r, g, b])
            #self.board.send_sysex(0x72, [pixel, r, g, b])
            self.logger.log_activity('changed pixel val {} to {}:{}:{}'.format(pixel, r, g, b))
        else:
            self.logger.log_activity('pixel value remained the same')
    
    def send_range_pixel(self, startpixel, endpixel, r, g, b):
        has_changed = False
        for i in range(startpixel, endpixel):
            if self.strip.change_pixel_value(i, r, g, b):
                has_changed = True
                break
        if has_changed:
            self.add_send(proto.RANGE_NEOPIXEL, [startpixel, endpixel, r, g, b])
            self.logger.log_activity('set range {}-{} to {},{},{}'.format(startpixel, endpixel, r, g, b))
        else:
            self.logger.log_activity('pixel values have not changed nothing send to arduino')

    """def show_strip(self):
        if not self.strip.has_been_shown():
            self.strip.show()
            self.add_send(NEOPIXEL_SHOW, [])
            self.logger.log_activity('strip is being shown')
        else:
            self.logger.log_activity('strip does not need to be shown')"""

    def handle_register_response(self):
        print("Register_response")

    def close(self):
        self.running = False
        self.logger.log_task_start("Safe Close Arduino")
        self.recv_future.result()
        self.send_future.result()
        self.logger.log_task_stop("Safe Close Arduino")
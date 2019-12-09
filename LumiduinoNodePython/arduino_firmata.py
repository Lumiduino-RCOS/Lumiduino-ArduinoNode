from pyfirmata import Arduino, util
import time
import threading
import queue
import concurrent.futures
from LumiduinoNodePython.customlogger import CustomLogger

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

        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.recv_future = None
        self.send_future = None
        
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
        while True:
            time.sleep(1)
        self.logger.log_task_stop("Stopping recv processing for arduino")

    def send_thread(self):
        """ Firmata will error if commands are sent too quickly"""
        self.logger.log_task_start("Starting send queue processing for arduino")
        while True:
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
        self.add_send(NEOPIXEL_REGISTER, [pin, count])
        #self.board.send_sysex(0x74, [pin, count])
        self.logger.log_activity('registered new strip on pin {} with lenght {}'.format(pin, count))
    
    def send_pixelval(self, pixel, r, g, b):
        self.add_send(NEOPIXEL_SET, [pixel, r, g, b])
        #self.board.send_sysex(0x72, [pixel, r, g, b])
        self.logger.log_activity('changed pixel val {} to {}:{}:{}'.format(pixel, r, g, b))

    def show_strip(self):
        self.add_send(NEOPIXEL_SHOW, [])
        self.logger.log_activity('strip is being shown')
        
    def handle_register_response(self):
        print("Register_response")
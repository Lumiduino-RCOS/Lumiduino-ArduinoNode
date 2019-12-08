from pyfirmata import Arduino, util
import time
import threading
import queue

NEOPIXEL_SET = 0x72
NEOPIXEL_REGISTER = 0x74
NEOPIXEL_SHOW = 0x80

class FirmataArduino():

    def __init__(self, port):
        self.send_queue = queue.Queue(maxsize=30)

        self.board = Arduino(port, baudrate=115200)
        self.board.add_cmd_handler(0x80, self.handle_register_response)
        self.board.add_cmd_handler(0x81, self.handle_register_response)
        print("connected port")
        threading.Thread(target=self.recv_thread).start()
        threading.Thread(target=self.send_thread).start()
        '''while True:
            self.board.digital[13].write(1)
            time.sleep(1)
            self.board.digital[13].write(0)
            time.sleep(1)'''

    def recv_thread(self):
        while True:
            time.sleep(1)
            #if self.board.bytes_available():
            #self.board.iterate()

    def send_thread(self):
        """ Firmata will error if commands are sent too quickly"""
        while True:
            try:
                (command, args) = self.send_queue.get(timeout=1)
                self.board.send_sysex(command, args)
                time.sleep(.004)
            except queue.Empty:
                continue
    
    def add_send(self, command: bytes, args: list):
        self.send_queue.put((command, args))

    def register_strip(self, pin: int, count: int):
        self.add_send(NEOPIXEL_REGISTER, [pin, count])
        #self.board.send_sysex(0x74, [pin, count])
        print('registered new strip on pin {} with lenght {}'.format(pin, count))
    
    def send_pixelval(self, pixel, r, g, b):
        self.add_send(NEOPIXEL_SET, [pixel, r, g, b])
        #self.board.send_sysex(0x72, [pixel, r, g, b])

    def show_strip(self):
        self.add_send(NEOPIXEL_SHOW, [])
    
    def handle_register_response(self):
        print("Register_response")
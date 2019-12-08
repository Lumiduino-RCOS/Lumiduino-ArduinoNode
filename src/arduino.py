import serial
import serial.tools.list_ports
from model.statedefinitions import ArduinoState
from controllers.observer import Observer
from controllers.subject import Subject
import threading
from queue import Queue
import io

class Arduino(Subject):

    def __init__(self, arduino_index=0):
        super().__init__()
        self.state = ArduinoState.STARTUP
        self.send_queue = Queue()
            arduino_list = self.find_arduinos(serial.tools.list_ports.comports())
            active_arduino = arduino_list[arduino_index]
            self.serial_connection = serial.Serial(active_arduino.device)
            self.state = ArduinoState.CONNECTED
            threading.Thread(target=self.read_loop).start()
            threading.Thread(target=self.write_loop).start()
        except Exception as err:
            print(err)
            self.state = ArduinoState.ERROR
        
    def read_loop(self):
        while self.serial_connection.is_open:
            #print("awaiting message")
            message = self.serial_connection.read_until(b'\n')
            #print("message", message)
            self.subject_state = message
            self._notify()

    def write_loop(self):
        while(self.serial_connection.is_open):
            try:
                message = self.send_queue.get(timeout=1)
                self.serial_connection.writelines([message])
            except:
                continue

    def write_lighting(self, device_addr, frame:):
        # create lighting message

    @staticmethod
    def find_arduinos(serial_object_list: list):
        arduinos = []
        for i in serial_object_list:
            if "Arduino" in i.manufacturer:
                arduinos.append(i)
                print(i)
        return arduinos


class obs(Observer):
    def update(self, arg):
        print(arg)
        return super().update(arg)

a = Arduino()
o = obs()
a.attach(o)
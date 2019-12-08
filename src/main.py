from arduino_firmata import FirmataArduino

import time

nar = FirmataArduino('/dev/ttyACM0')
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
    nar.show_strip()

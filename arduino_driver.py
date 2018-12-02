import serial
import serial.tools.list_ports
import os
import time

TIME_BETWEEN_MESSAGES = 0.01
AMBIENT_LIGHT_BYTE = 89
PARTY_LIGHT_BYTE = 167
WAIT_FOR_ANSWER_BYTE = 65


def _get_port():
    if os.name == 'nt':  # if run on windows
        ports = [str(port) for port in serial.tools.list_ports.comports()]

        assert len(ports) > 0, 'no serial port found'
        return ports[-1].split('-')[0].strip()
    else:  # linux support
        return '/dev/ttyACM0' # and lets pray


class ArduinoController:
    def __init__(self):
        self._serial_port = _get_port()

        self.ser = serial.Serial(self._serial_port, 9600)
        self._data = None
        self._run_thread = True

        self.set_ambient()

    def disconnect(self):
        self.ser.close()

    # Set a color to a desired LED by controlling the RGB values
    def set_ambient(self):
        #print('set ambient')
        values = bytearray([AMBIENT_LIGHT_BYTE])
        self.ser.write(values)

    def set_party(self):
        #print('set party')
        values = bytearray([PARTY_LIGHT_BYTE])
        self.ser.write(values)

    def set_wait_for_answer(self):
        #print('set wait for answer')
        values = bytearray([WAIT_FOR_ANSWER_BYTE])
        self.ser.write(values)

    def read_button(self):
        if self.ser.inWaiting() == 0:
            return False
        line = self.ser.readline()
        try:
            line = line.decode('UTF-8').rstrip("\r\n")
        except:
            return False

        if line == 'k':
            return True

        return False

    def flush_serial(self):
        while self.ser.inWaiting():
            self.ser.readline()


if __name__ == '__main__':
    ar = ArduinoController()
    while True:
        ar.set_ambient()
        input("Press Enter to continue...")
        ar.set_party()
        input("Press Enter to continue...")
        ar.set_wait_for_answer()
        input("Press Enter to continue...")
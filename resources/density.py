import serial

# constants
DESIGN_ERROR = 4.4
FIXED_LENGTH = 200 + DESIGN_ERROR  # In millimeter
IR = 35  # In millimeter
PI = 3.14
HT = 155  # In millimeter

# wt_serial = serial.Serial('COM6', 1200, timeout=1)
# wt_serial = serial.Serial('COM10', 9600, timeout=1)


class Density:

    def __init__(self):
        print('Object Initialized')

    def get_params(self):
        # return self.calculation(self.weight(), self.laser())
        return 'hello'

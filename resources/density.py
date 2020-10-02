import serial

# constants
FIXED_LENGTH = 200  # In millimeter
IR = 35  # In millimeter
PI = 3.14
HT = 155  # In millimeter

wt_serial = serial.Serial('COM6', 1200, timeout=1)
lsr_serial = serial.Serial('COM13', 9600, timeout=1)


class Density:

    def __init__(self):
        print('Object Initialized')

    def weight(self):  # o/p: weight
        count = 0
        avg_weight = 0.0
        while(count < 5):  # averaging weight for 5 values
            if(wt_serial.in_waiting > 0):  # Wait until there is data waiting in the serial buffer
                count += 1
                wt_serial.flushInput()
                wt_serial.read_until()  # to flush any remaining data half cleared data
                # Read data out of the buffer until a carraige return / new line is found
                serialString = wt_serial.readline()
                # decode byte data into string
                wtraw_data = serialString.decode('ascii')
                # getting weight value from the string
                string_weight = wtraw_data[2:9]
                # print(count,float(string_weight));
                avg_weight += float(string_weight)
        weight = round(avg_weight / 5, 2)
        self.weight_raw_output = weight
        # print(avg_weight,weight)
        return weight

    def laser(self):  # o/p: distance
        if(lsr_serial.in_waiting > 0):
            distance = 0
            serialString = lsr_serial.read(11)
            data = serialString.hex()
            # print(data)
            # print(data[15:18])
            intdata = int(data[15:18], 16)  # hexa value
            # print(intdata)
            if(intdata == 0):
                distance = 0
            else:
                distance = 163/3285 * (intdata-810) + 119.5
            distance = round(distance, 2)
            # print(distance,"mm")
            self.laser_raw_output = distance
            return distance

    def calculation(self, wt_rawop, lsr_rawop):  # ip: lsr_rawop & wt_rawop
        orad = FIXED_LENGTH - lsr_rawop + 35
        vol = PI * ((orad * orad - IR * IR)/10000) * (HT/100)
        self.volume = vol
        mass = wt_rawop
        self.mass = mass
        density = round((mass/vol), 2)
        self.density = density
        self.outer_radius = orad
        print("odia ", round(orad*2, 2), "mass ", mass, "Density ", density)
        return {'volume': self.volume,
                'mass': self.mass,
                'outer_radius': self.outer_radius,
                'density': self.density,
                'laser_raw_output': self.laser_raw_output,
                'weight_raw_output': self.weight_raw_output}

    def get_params(self):
        return self.calculation(self.weight(), self.laser())

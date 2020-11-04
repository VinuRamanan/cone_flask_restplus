''' Density calculation using ssm calculation and try catch
for serial port and correct substring function
'''

import serial

# data from front end at initialization and when changed
DESIGN_ERROR = 4.4  # calibration of sensor for compensating maufacturing error
TUBE_RAD = 0.35  # In millimeter


# constants
FIXED_LENGTH = 200 + DESIGN_ERROR  # In millimeter
PI = 3.14  # pi value
TO_DECIMETER = 1/100  # length from millimeter to decimeter for litre conversion
To_MILLIMETER = 100  # length decimeter to millimeter for litre conversion

# initialization
weight_object = None
laser_object = None

# opening Serial ports


# initilazing weight machine comport using try   $$ ip: comport name @@ op: weight machine object
def weight_machine_config(comport):
    try:
        wt_serial = serial.Serial(comport, 1200, timeout=1)
        return wt_serial
    except serial.SerialException as err:
        print("Weight Machine Configuration Failed ", err)
        return None


# initilazing laser sensor comport using try  $$ ip: comport name @@ op: laser sensor object
def laser_sensor_config(comport):
    try:
        lsr_serial = serial.Serial(comport, 9600, timeout=1)
        return lsr_serial
    except serial.SerialException as err:
        print("Laser Sensor Configuration Failed ", err)
        return None


# to get a substring between the two characters $$ ip: 1.string 2.start char 3.End char @@ op: data between that two chars
def find_between(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


def float_conv(data):  # float conversion using try $$ ip:string  @@ op: float (or) Error
    try:
        return float(data)
    except ValueError:
        print("Float conversion error")


def weight(object):  # weight finder using average of 5 $$ ip: weight mc object @@ op: weight in grams
    count = 0
    avg_weight = 0.0
    while(count < 5):  # averaging weight for 5 values
        if(object.in_waiting > 0):  # Wait until there is data waiting in the serial buffer
            count += 1
            object.flushInput()  # to clear old data from serial buffer
            object.read_until()  # to flush any remaining data half cleared data
            # Read data out of the buffer until a carraige return / new line is found
            serialString = object.readline()
            # print(serialString)
            # decode byte data into string
            wtraw_data = serialString.decode('ascii')
            # getting weight value from the string
            string_weight = find_between(wtraw_data, '+', 'g')
            # print(float_conv(string_weight))
            avg_weight += float_conv(string_weight)
    weight = float_conv(avg_weight / 5)
    #print("Weight :",weight)
    return weight


def laser(object):  # to find distance bwt laser sensor and ouside of yarn $$Ip: laser object o/p: distance in mm
    if(object.in_waiting > 0):
        distance_bwt_yarnOut_and_sensor_mm = 0
        # read string of 11 char of current sensor value
        current_sensor_String = object.read(11)
        # convert string of current sensor value to hex
        current_sensor_hexvalue = current_sensor_String.hex()
        # print(current_sensor_hexvalue)
        # print(current_sensor_hexvalue[15:18])
        # seperate required current sensor from total hexa value
        current_sensor_Intvalue = int(current_sensor_hexvalue[15:18], 16)
        # print(current_sensor_Intvalue)
        if(current_sensor_Intvalue == 0):
            distance_bwt_yarnOut_and_sensor_mm = 0
        else:
            # current digital value to distance of yarn to sensor
            distance_bwt_yarnOut_and_sensor_mm = 163 / \
                3285 * (current_sensor_Intvalue-810) + 119.5
        # distance between laser sensor and yarn outside
        distance_bwt_yarnOut_and_sensor_mm = round(
            distance_bwt_yarnOut_and_sensor_mm, 2)
        # print("Laser")
        #print("Laser raw op:",distance_bwt_yarnOut_and_sensor_mm,"mm")
        return distance_bwt_yarnOut_and_sensor_mm


# ip: traverse star, traverse end, wt_rawop & lsr_rawop
def calculation(tra_start, tra_end, wt_rawop, lsr_rawop, output):
    # traverse starting length
    tra_start_dm = float_conv(tra_start) * TO_DECIMETER
    tra_end_dm = float_conv(tra_end) * TO_DECIMETER  # traverse ending length
    __weight = float_conv(wt_rawop)  # weight in grams
    # yarn winded cone radius in decimeter
    yarncone_rad_dm = float_conv(
        (FIXED_LENGTH - lsr_rawop + 35) * TO_DECIMETER)
    # depth of the frustrated cone divided by two because two cones in top and bottom
    depth_of_frustrated_cone = (tra_start_dm - tra_end_dm) / 2
    cylinder_vol = float_conv(
        PI * yarncone_rad_dm * yarncone_rad_dm * tra_end_dm)  # yarn cylinder volume
    frustrated_con_vol = float_conv(0.33 * PI * depth_of_frustrated_cone *
                                    (TUBE_RAD * TUBE_RAD + yarncone_rad_dm * TUBE_RAD + yarncone_rad_dm * yarncone_rad_dm))  # frustrated cone volume
    empty_cylinder_vol = float_conv(
        PI * TUBE_RAD * TUBE_RAD * tra_start_dm)  # empty cheese volume
    # total volume = yarn cylinder + 2 * frustarted cone (top and bottom) - empty cheese
    volume = cylinder_vol + frustrated_con_vol * 2 - empty_cylinder_vol
    output['volume'] = volume
    __density = round(float_conv(weight/volume), 2)  # yarn density in gpl
    # yarncone diameter in mm
    __yarncone_dia_mm = round(yarncone_rad_dm * 2 * To_MILLIMETER, 2)
    output['outer_diameter'] = __yarncone_dia_mm
    __weight = round(float_conv(wt_rawop), 2)
    output['weight'] = weight
    #print("Cone Dia :",yarncone_dia_mm)
    # print(__density)
    return __density


def calculate(tra_start, tra_end, weight_object, laser_object):
    if weight_object and laser_object:
        #print("Com port setup finished")
        #print("Check poimt 1")
        output = {}
        wt_rawop = float(weight(weight_object))
        output['weight_raw_output'] = wt_rawop
        lsr_rawop = float(laser(laser_object))
        output['laser_raw_output'] = lsr_rawop
        # tra_start = input("Enter the tra_start :") # from front end ( height start )
        # tra_end = input("Enter the tra_end :") # from front end ( height end )
        density = calculation(tra_start, tra_end, wt_rawop, lsr_rawop, output)
        output['density'] = density
        print("Wt: ", wt_rawop, "den: ", density)
        return output


def hardware_config(wt_comport="COM10", lsr_comport="COM6"):
    global weight_object, laser_object
    weight_object = weight_machine_config(wt_comport)
    laser_object = laser_sensor_config(lsr_comport)


# hardware_config()

# while(1):
#     a = input("Do u want to check ? 1/0 : ")
#     if (a == "1"):
#         calculate(147,135)

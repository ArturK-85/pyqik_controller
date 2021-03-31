import os
import serial
import time
import pickle
import ctypes

qik_controll_table = {"Firmware_Version": 0x81,
                      "Get_Error": 0x82,
                      "Get_Conf": 0x83,
                      "Set_Conf": 0x84,
                      "Motor0_Coast": 0x86,
                      "Motor1_Coast": 0x87,
                      "Motor0_Fwd": 0x88,
                      "Motor0_Rev": 0x8A,
                      "Motor1_Fwd": 0x8C,
                      "Motor1_Rev": 0x8E}

class CRC(object):
    """ CRC class returning CRC7 code for Pololu Qik serial communication
        using a modify C code as a library with ctypes to a fast computation
        CRC7 checksum. """

    def __init__(self):
        """ As init load modify C code library """
        sharedObjectPath = (os.getcwd() + "/" + "pololu_crc7.so")
        self.crc = ctypes.CDLL(sharedObjectPath)

    def checksum(self, message_hex):
        """ Usage get_crc7(message_array, lenght_of_array) """

        check_len = hasattr(message_hex, '__len__')

        if check_len is True:
            msg_len = len(message_hex)
            message_hex = (ctypes.c_ubyte * msg_len)(* message_hex)
        else:
            msg_len = 1
            message_hex = (ctypes.c_ubyte * msg_len)(message_hex)

        result = self.crc.get_crc7(message_hex, msg_len)
        return result

class ErrorCheck(CRC):

    def error_check(self):
        index = 0
        message = qik_controll_table.get("Get_Error")

        self.write_port(message)
        time.sleep(0.004)

        self.read_data = self.read_port()

        msg_bin = int(self.read_data)

        error_table = {3: 'Data Overrun Error',
                       4: 'Frame Error',
                       5: 'CRC Error',
                       6: 'Format Error',
                       7: 'Timeout'}

        bit_ignore = [0, 1, 2]

        while msg_bin:           # returns true if data is no 0
            if msg_bin & 1:      # returns true if LSB is 1
                if index in bit_ignore:
                    pass
                else:
                    print(error_table.get(index))
            msg_bin >>= 1         # discard LSB
            index += 1

class PortControll(ErrorCheck):

    def read_port(self):
        self.read_data = self.ser.read().encode('hex')
        return self.read_data

    def write_port(self, message):
        check_len = hasattr(message, '__len__')
        crc = self.get_crc.checksum(message)
        packet = []

        if check_len is True:
            msg_len = len(message)

            for i in range(msg_len):
                packet.append(message[i])

        else:
            msg_len = 1
            packet.append(message)

        packet.append(crc)

        self.ser.write(packet)
        time.sleep(0.004)

    def port_close(self):
        self.ser.close()

class ControllerInit(PortControll):
    def __init__(self, device_path, speed):
        self.string = ''
        print("Pololu Qik Python Library\n")

        #Max baurate 38400 kbps
        self.device_path = device_path
        self.speed = speed
        self.ser = serial.Serial(self.device_path, self.speed)
        print('Serial Port Open as {0}, on speed {1} kbps'.format(self.device_path, self.speed))

        #If your qik is set to automatically detect the baud,
        #you must first send it the byte 0xAA (170) in order
        #to exit autodetect mode and enter normal operation
        self.ser.write([0xAA])
        self.get_crc = CRC()

    def get_conf(self):
        #Configuration parameters:
        # 0 - Device Id
        # 1 - PWM Parameter :
        #    0 = high-frequency, 7-bit mode (PWM frequency of 31.5 kHz)
        #    1 = high-frequency, 8-bit mode (PWM frequency of 15.7 kHz)
        #    2 = low-frequency, 7-bit mode (PWM frequency of 7.8 kHz)
        #    3 = low-frequency, 8-bit mode (PWM frequency of 3.9 kHz)
        # 2 - Shutdown Motors on Error:
        #    1 is On, 0 is Off
        # 3 - Serial Timeout:
        #    1 is On, 0 is Off

        self.get_conf_addr = qik_controll_table.get("Get_Conf")

        # Check Device Id
        message = self.get_conf_addr, 0x01
        self.write_port(message)

        self.data = self.read_port()
        print('Device ID: {0}'.format(self.data))

        time.sleep(0.01)

        #Check PWM parameters
        message = self.get_conf_addr, 0x01
        self.write_port(message)

        self.data = self.read_port()

        if self.data == "00":
            self.string = "Frequency is 31.5kHz"

        elif self.data == "01":
            self.string = "Frequency is 15.7kHz"

        elif self.data == "02":
            self.string = "Frequency is 7.8kHz"

        elif self.data == "03":
            self.string = "Frequency is 3.9kHz"

        print('PWM Parameter: {0}'.format(self.string))

        time.sleep(0.01)

        #Check Motor Shutdown Parameter
        message = self.get_conf_addr, 0x02
        self.write_port(message)

        self.data = self.read_port()

        if self.data == "00":
            self.string = "Off"
        else:
            self.string = "On"

        print('Shutdown Motors on Error: {0}'.format(self.string))

        time.sleep(0.01)

        #Check Serial Timeout
        message = self.get_conf_addr, 0x03
        self.write_port(message)

        self.data = self.read_port()
        print('Serial Timeout: {0}'.format(self.data))

    def set_conf(self, id, pwm, err, timeout):
        set_conf_addr = qik_controll_table.get("Set_Conf")

        message = set_conf_addr, 0x00, id, 0x55, 0x2A
        self.write_port(message)

        message = set_conf_addr, 0x01, pwm, 0x55, 0x2A
        self.write_port(message)

        message = set_conf_addr, 0x02, err, 0x55, 0x2A
        self.write_port(message)

        message = self.set_conf_addr, 0x03, timeout, 0x55, 0x2A
        self.write_port(message)

class MotorController(ControllerInit):

    def motor_coast(self, motor_no):

        if motor_no == 0:
            get_motor_addr = qik_controll_table.get("Motor0_Coast")

        elif motor_no == 1:
            get_motor_addr = qik_controll_table.get("Motor1_Coast")

        message = get_motor_addr
        self.write_port(message)

    def motor_run(self, motor_no, dir, speed):

        if dir == "Fwd" and motor_no == 0:
            self.get_motor_addr = qik_controll_table.get("Motor0_Fwd")

        elif dir == "Fwd" and motor_no == 1:
            self.get_motor_addr = qik_controll_table.get("Motor1_Fwd")

        elif dir == "Rev" and motor_no == 0:
            self.get_motor_addr = qik_controll_table.get("Motor0_Rev")

        elif dir == "Rev" and motor_no == 1:
            self.get_motor_addr = qik_controll_table.get("Motor1_Rev")

        message = self.get_motor_addr, speed
        self.write_port(message)

    def motor_stop(self):
        message = self.get_motor_addr, 0x00
        self.write_port(message)

import serial
import time
import re
#from messaging.sms import SmsDeliver


class CallAction():
    def __init__(self, number):
        self.number = number

    def call_to_open(self):
        #return print("valve opened!")
        self.connect_phone()
        command_to_hang_off = "ATH\r"
        self.ser.write(command_to_hang_off.encode())
        time.sleep(2)
        command = "ATD{};\r".format(self.number)
        self.ser.write(command.encode())
        print("call sent to open valve")
        time.sleep(10)
        return print("valve opened!")

    def call_to_close(self):
        #return print("valve closed!")
        self.connect_phone()
        command_to_hang_off = "ATH\r"
        self.ser.write(command_to_hang_off.encode())
        time.sleep(2)
        command = "ATD{};\r".format(self.number)
        self.ser.write(command.encode())
        print("call sent to close valve")
        time.sleep(10)
        return print("valve closed!")

    def connect_phone(self):
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=20)


    def send_command(self,com):
        self.ser.write(com.encode())
        time.sleep(2)
        ret = []
        while self.ser.inWaiting() > 0:
            msg = self.ser.readline().strip()
            if msg!="":
                ret.append(msg)
        return ret

    def get_income_sms_message(self):
        time.sleep(2)
        ret = []
        msg = b""
        while b"CMTI" not in msg:
            msg = self.ser.readline().strip()
            if msg != b"":
                ret.append(msg)
        sms = self.get_sms_from_income_signal(ret)
        return sms

    def get_sms_from_income_signal(self, signal):
        index = re.findall(r'\d+', signal)
        command = "AT+CMGR={}\r".format(index[0])
        self.ser.write(command.encode())
        ret = []
        msg = b""
        while b"OK" not in msg:
            msg = self.ser.readline().strip()
            if msg != b"":
                ret.append(msg)
        return ret

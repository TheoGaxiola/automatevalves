import serial
import time
import re
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
gpio_output = 7
GPIO.setup(gpio_output, GPIO.OUT)

class CallAction():
    def __init__(self, number, valve_name=None, admin_tel=None):
        self.number = number
        self.valve_name = valve_name

    def call_to_open(self):
        #return print("valve opened!")
        self.connect_phone()
        command_to_hang_off = "ATH\r"
        self.ser.write(command_to_hang_off.encode())
        time.sleep(2)
        command = "ATD{};\r".format(self.number)
        self.ser.write(command.encode())
        print("call sent to open valve")
        sms_confirmation = self.detect_valve_opened()
        if sms_confirmation:
            self.send_sms("Valve opened confirmation", 3314680990)
            return print("valve opened!")
        else:
            self.send_sms("No hubo respuesta de gsm relay de {}, la bomba fue apagada por seguridad".format(self.valve_name)) #3rd cellphone number pending
            self.emergency_pump_stop()
            return print("error in valve open process")

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
        sms = self.get_sms_from_income_signal(ret[0])
        return sms

    def get_sms_from_income_signal(self, signal):
        index = re.findall(r'\d+', signal.decode())
        command = "AT+CMGR={}\r".format(index[0])
        self.ser.write(command.encode())
        ret = []
        msg = b""
        while b"OK" not in msg:
            msg = self.ser.readline().strip()
            if msg != b"":
                ret.append(msg)
        return ret

    def detect_valve_opened(self):
        sms = self.get_income_sms_message()
        for i in sms:
            if b"openedOperated" in i:
                return True
            else:
                return False

    def detect_valve_closed(self):
        sms = self.get_income_sms_message()
        for i in sms:
            if b"closedOperated" in i:
                return True
            else:
                return False

    def send_sms(self, msg, number=None):
        command = 'AT+CMGF=1\r'
        self.ser.write(command.encode())
        time.sleep(0.5)

        command = 'AT+CMGS="{}"\r'.format(number)
        self.ser.write(command.encode())
        time.sleep(0.5)

        cmd = '{}\r'.format(msg)
        self.ser.write(cmd.encode())
        time.sleep(0.5)

        self.ser.write(bytes([26]))

        time.sleep(0.5)

    def emergency_pump_stop(self):
        GPIO.output(gpio_output, GPIO.HIGH)
        return True
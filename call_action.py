import serial
import time
from messaging.sms import SmsDeliver


class CallAction():
    def __init__(self, number):
        self.number = number

    def call_to_open(self):
        return None

    def call_to_close(self):
        return None

    def connect_phone(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)

    def get_new_sms_response(self):
        print("SENDING HELLO")
        com="ERROR"
        count=0
        while(com!="OK"):
            com=sendCommand("AT")[0]
            count+=1
            if(count>5):
            print "COULD NOT GET A HELLO, all I got was "+com
            return
        print(send_command("AT+CMGF=0")[0])

        while(True):
            sms = self.read_sms()

            for s in sms:
            print ""
            print "SMS"
            response = s.text
            time.sleep(1)
            if response is not None:
                    killSMS()
            return response

    def read_sms(self):
        print("LOOKING FOR SMS")
        list = send_command("AT+CMGL=0")
        ret = []
        for item in list:
            #print item
                if item.startswith("+CMGL:") == False:
            if item!="OK":
                ret.append(SmsDeliver(item))
        return ret

    def send_command(self,com):
        ser.write(com+"\r\n")
        time.sleep(2)
        ret = []
        while ser.inWaiting() > 0:
            msg = ser.readline().strip()
            msg = msg.replace("\r","")
            msg = msg.replace("\n","")
            if msg!="":
            ret.append(msg)
        return ret

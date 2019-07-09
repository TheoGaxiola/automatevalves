import serial
import time
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
        self.ser = serial.Serial('/dev/ttyS0', 9600)

    def get_new_sms_response(self):
        print("SENDING HELLO")
        com="ERROR"
        count=0
        while(com!="OK"):
            com=sendCommand("AT\r")[0]
            count+=1
            if(count>5):
                print ("COULD NOT GET A HELLO, all I got was ",com)
            return
        print(send_command("AT+CMGF=0\r")[0])

        while(True):
            sms = self.read_sms()

            for s in sms:
                print ("")
                print ("SMS")
                response = s.text
                time.sleep(1)
                if response is not None:
                    killSMS()
            return response

    def read_sms(self):
        print("LOOKING FOR SMS")
        list = self.send_command("AT+CMGL=0\r")
        ret = []
        for item in list:
            #print item
            #if item.startswith("+CMGL:") == False:
            #    if item!="OK":
                  #  ret.append(SmsDeliver(item))
            ret.append(item)
        return ret

    def send_command(self,com):
        self.ser.write(com.encode())
        time.sleep(2)
        ret = []
        while self.ser.inWaiting() > 0:
            msg = self.ser.readline().strip()
            #msg = msg.decode().replace("\r","")
            #msg = msg.decode().replace("\n","")
            if msg!="":
                ret.append(msg)
        return ret

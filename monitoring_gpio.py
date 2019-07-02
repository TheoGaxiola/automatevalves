from call_action import CallAction
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
banOpen2 = 0
banClose2 = 0
banOpen3 = 0
banClose3 = 0

#creating an CallAction instance for each valve
valve1 = CallAction(3314680990)
valve2 = CallAction(6737321192)

#raspberry pi gpio inputs assignment for each valve
valve1_input = 16
valve2_input = 12
GPIO.setup(valve1_input,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(valve2_input,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    print(GPIO.input(valve1_input))
    print(GPIO.input(valve2_input))
    sleep(.5)
    if GPIO.input(valve1_input) == 1:
        if banOpen2 == 0:
            sleep(.5)
            valve1.call_to_open()
            banOpen2 = 1
            banClose2 = 0
            sleep(.5)
    if GPIO.input(valve1_input) == 0:
        if banClose2 == 0:
            sleep(.5)
            valve1.call_to_close()
            banClose2 = 1
            banOpen2 = 0
            sleep(.5)        
    if GPIO.input(valve2_input) == 1:
        #print("INICIO VALVE 2")
        if banOpen3 == 0:
            sleep(.5)
            #print("hola valve2")
            valve2.call_to_open()
            banOpen3 = 1
            banClose3 = 0
            sleep(.5)
    if GPIO.input(valve2_input) == 0:
        #print("hola inicio valve 2 valor 0")
        if banClose3 == 0:
            sleep(.5)
            valve2.call_to_close()
            banClose3 = 1
            banOpen3 = 0

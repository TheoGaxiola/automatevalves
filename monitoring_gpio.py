from call_action import CallAction

banOpen2=0
banClose2=0
banOpen3=0
banClose3=0
valve1 = CallAction(3314680990)
valve2 = CallAction(6737321192)

while True:
    if gpio(2) == 1:
        if banOpen2 == 0:
            valve1.call_to_open()
            banOpen2 = 1
            banClose2 = 0
    elif gpio(2) == 0:
        if banClose2 == 0:
            valve1.call_to_close()
            banClose2 = 1
            banOpen2 = 0
    elif gpio(3) == 1:
        if banOpen3 == 0:
            valve2.call_to_open()
            banOpen3 = 1
            banClose3 = 0    
    elif gpio(3) == 0:
        if banClose3 == 0:
            valve2.call_to_close()
            banClose3 = 1
            banOpen3 = 0

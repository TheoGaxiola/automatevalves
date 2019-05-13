class CallAction():
    def __init__(self, number):
        self.number = number

    def call_to_open(self):
	return None

    def call_to_close(self):
	return None

    def connect_phone(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)

    def wait_for_sms_response(self):
	return None

    	

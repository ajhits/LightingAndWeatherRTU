
import serial
import threading

import time
class Serial:
    def __init__(self,app=None, firebase=None):
        self.serial = serial
        self.Ser = None
        self.Firebase = firebase()
        self.timeout  = 1
        self.port     = "COM4"
        self.baudrate = 9600
        
        self.message = "nag reset"

        if app is not None:
            self.timeout  = app.config.get("SERIAL_TIMEOUT")
            self.port     = app.config.get("SERIAL_PORT")
            self.baudrate = app.config.get("SERIAL_BAUDRATE")
            
        self.init_app()
    
    # Initialize Application
    def init_app(self):

        self._thread = threading.Thread(target=self.__open_serial,daemon=True)
        self._thread.start()

    
    # Open Serial Port
    def __open_serial(self):
        try:
            self.Ser = self.serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print("serial is open")
            
            while True:
                last_trigger_time = time.time()
                if self.Ser.in_waiting > 0:
                    data = self.Ser.readline().decode().strip()
                    message = data.split(",")
        
                    
                    self.verify_serial(data=bool(int(message[0])),text="person in")
                    self.verify_serial(data=bool(int(message[1])),text="person out")
            
                

                    
        except Exception as e:
            print(e)
            pass

    # get serial message
    def get_serial_message(self):
        print(self.message)
        return self.message
    
    def verify_serial(self,data,text):
        last_trigger_time = time.time()
        if data:
            print(text)
            self.Firebase.firebase_insert({
            "person_status": text,
            "last_trigger_time": last_trigger_time
        })
        
        



import serial
import threading
import time

class Serial:
    def __init__(self,app=None):
        self.serial = serial
        self.Ser = None
        
        self.timeout  = 1
        self.port     = "COM7"
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
                if self.Ser.in_waiting > 0:
                    data = self.Ser.readline().decode().strip()
                    self.message = data
                    print(self.message)
                

                    
        except Exception as e:
            print(e)
            pass

    # get serial message
    def get_serial_message(self):
        print(self.message)
        return self.message
        


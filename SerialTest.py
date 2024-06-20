
import serial
import threading
import time

class Serial:
    def __init__(self,app):
        self.serial = serial
        self.Ser = None

        if app is not None:
            self.timeout  = app.config.get("SERIAL_TIMEOUT")
            self.port     = app.config.get("SERIAL_PORT")
            self.baudrate = app.config.get("SERIAL_BAUDRATE")
            self.init_app()
    
    # Initialize Application
    def init_app(self):
        print("running")
        self._thread = threading.Thread(target=self.__open_serial)
        self._thread.setDaemon(True)
        self._thread.start()

    
    # Open Serial Port
    def __open_serial(self):
        try:
            self.Ser = self.serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print("serial is open")
        except Exception as e:
            print(e)
            pass

    # get serial message
    def get_serial_message(self):
        
        while self.Ser is None:
            # Add some delay to avoid busy-waiting
            time.sleep(0.1)
        
        try:
            
            data = self.Ser.readline().decode().strip()
            print(data)
            return data
        except Exception as e:
            return e
        
        
        
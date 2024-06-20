import serial
import time

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what your Arduino is connected to.
ser = serial.Serial('COM5', 9600,timeout=1)  # Change 'COM3' to your Arduino's serial port

def read_data_from_arduino():
    if ser.in_waiting > 0:

        data = ser.readline().decode().strip()
        return data


while True:
    response = read_data_from_arduino()
    print(f"Response from Arduino: {response}")
    time.sleep(1)



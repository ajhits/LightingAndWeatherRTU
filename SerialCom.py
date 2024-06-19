from flask import Flask, render_template, Response, request
import serial
import time



ser = serial.Serial('COM7', 9600)
ser.timeout = 1


# Define the serial port and baud rate
ser.reset_input_buffer()

ser.flush()
data = ser.readline().decode('utf-8').rstrip()
print(data)
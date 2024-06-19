from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from model.Object_detection import ObjectDetector

import time
import serial
import cv2

class MainWindow(QtWidgets.QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        # Define the serial port and baud rate
        self.ser = serial.Serial('COM8', 9600, timeout=1)  # Replace 'COM3' with the correct port name
        
        # Create an instance of the ObjectDetector class
        self.object_detector = ObjectDetector(model='model/ssd_mobilenet_v2.tflite')
        self.object_detector.run()
        
        # for video streaming variable
        self.videoStream = cv2.VideoCapture(0) 
        self.videoStream.set(4, 1080)

        # frame
        self.setObjectName("mainMenu")
        self.resize(1024, 565)
        
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1031, 571))
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.widget.setStyleSheet("background-color: #f5f5f5")
        self.widget.setObjectName("widget")
        
        # Video Streaming
        self.video = QtWidgets.QLabel(self.widget)
        self.video.setGeometry(QtCore.QRect(200, 20, 631, 451))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        self.video.setFont(font)
        self.video.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.video.setStyleSheet("border: 2px solid #30475E;\n"
"\n"
"")
        self.video.setScaledContents(True)
        self.video.setObjectName("video")
        
        # Person In
        self.video_5 = QtWidgets.QLabel(self.widget)
        self.video_5.setGeometry(QtCore.QRect(530, 490, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.video_5.setFont(font)
        self.video_5.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.video_5.setStyleSheet("color: #121212;")
        self.video_5.setScaledContents(True)
        self.video_5.setObjectName("video_5")
        
        # Person Out
        self.video_6 = QtWidgets.QLabel(self.widget)
        self.video_6.setGeometry(QtCore.QRect(360, 490, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        self.video_6.setFont(font)
        self.video_6.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.video_6.setStyleSheet("color: #121212;")
        self.video_6.setScaledContents(True)
        self.video_6.setObjectName("video_6")
        
        # Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.videoStreaming)
        self.timer.start()
        


        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Frame", "Frame"))
        self.video.setText(_translate("Frame", "Loading"))
        self.video_5.setText(_translate("Frame", "0 person OUT"))
        self.video_6.setText(_translate("Frame", "0 person IN"))
        
    # serial communication
    def ir_com(self):
        self.ser.reset_input_buffer()
        self.ser.flush()
        data =self.ser.readline().decode('utf-8').rstrip()
        print(data)
        
    # Video Streaming
    def videoStreaming(self):
        ret, frame = self.videoStream.read()
        
        self.ir_com()
        try:
        
            # object detection
            frame = cv2.flip(frame, 1)
            frame = self.object_detector.detect_objects(frame)
        except Exception as e:
            pass
            print(e)
        
        height, width, channel = frame.shape
        bytesPerLine = channel * width
        qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.video.setPixmap(pixmap)
        
if __name__ == "__main__":
        
    import sys
    # Create a new QApplication object
    app = QApplication(sys.argv)

    New_menu = MainWindow()
    New_menu.show() 

    sys.exit(app.exec_())
#!/usr/bin/python

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

# from model.Object_detection import ObjectDetector


class App(QtWidgets.QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        # Create an instance of the ObjectDetector class
        # self.object_detector = ObjectDetector(model='model/ssd_mobilenet_v2.tflite')
        # self.object_detector.run()
        
        # for video streaming variable
        # self.videoStream = cv2.VideoCapture(1) if cv2.VideoCapture(1).isOpened() else cv2.VideoCapture(0)
        # self.videoStream.set(4, 1080)
        
        # Frame
        self.setObjectName("Lightning weather system RTU")
        self.resize(1024, 565)
        self.setFrameShape(QtWidgets.QFrame.Box)
        
        self.setAutoFillBackground(False)
        self.setStyleSheet("background-color: rgb(231, 229, 213);\n")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setLineWidth(2)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # background widget
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1031, 571))
        self.widget.setStyleSheet("background-color: #f5f5f5")
        self.widget.setObjectName("widget")
        
        # video
        self.video = QtWidgets.QLabel(self.widget)
        self.video.setGeometry(QtCore.QRect(340, 90, 631, 451))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        self.video.setFont(font)
        self.video.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.video.setStyleSheet("border: 2px solid #30475E;\n"
"\n"
"color: #121212"
"")
        self.video.setScaledContents(False)
        self.video.setAlignment(QtCore.Qt.AlignCenter)
        self.video.setObjectName("video")
        
        # Title
        self.Title = QtWidgets.QLabel(self.widget)
        self.Title.setGeometry(QtCore.QRect(0, 20, 1021, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        self.Title.setFont(font)
        self.Title.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.Title.setStyleSheet("color: #121212\n"
"")
        self.Title.setScaledContents(False)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("video_2")
        
        # Person IN
        self.PersonIn = QtWidgets.QLabel(self.widget)
        self.PersonIn.setGeometry(QtCore.QRect(50, 110, 251, 191))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        self.PersonIn.setFont(font)
        self.PersonIn.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.PersonIn.setStyleSheet("border: 2px solid #30475E ;\n"
"border-radius: 50px;\n"
"color: #121212")
        self.PersonIn.setScaledContents(False)
        self.PersonIn.setAlignment(QtCore.Qt.AlignCenter)
        self.PersonIn.setObjectName("PersonIn")
        
        # Person Out
        self.PersonOut = QtWidgets.QLabel(self.widget)
        self.PersonOut.setGeometry(QtCore.QRect(50, 330, 251, 191))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(26)
        self.PersonOut.setFont(font)
        self.PersonOut.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.PersonOut.setStyleSheet("border: 2px solid #30475E ;\n"
"border-radius: 50px;\n"
"color: #121212")
        self.PersonOut.setScaledContents(False)
        self.PersonOut.setAlignment(QtCore.Qt.AlignCenter)
        self.PersonOut.setObjectName("PersonIn")
        
        # # timer
        # self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.videoStreaming)
        # self.timer.start(30)
        
        
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Frame", "lighthning weather"))
        self.video.setText(_translate("Frame", "Video itsadasdaso"))
        self.PersonIn.setText(_translate("Frame", "0\nperson in"))
        self.PersonOut.setText(_translate("Frame", "0\nperson out"))
        self.Title.setText(_translate("Frame", "Lightning AND Weather system in RTU"))
        
    #  # for video streaming
    # def videoStreaming(self):
    #     ret, frame = self.videoStream.read()
        
    #     # if no detected frames
    #     if not ret:
    #         self.video.setText("Please wait camera is loading")
    #         return
        
    #     # Object detection
    #     frame_with_objects = self.object_detector.detect_objects(frame)
        

    #     # display the frame on the label
    #     height, width, channel = frame_with_objects.shape
    #     bytesPerLine = channel * width
    #     qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_BGR888)
    #     pixmap = QtGui.QPixmap.fromImage(qImg)
    #     self.video.setPixmap(pixmap)

        
        
if __name__ == "__main__":

    import sys
    # Create a new QApplication object
    app = QApplication(sys.argv)

    New_menu = App()
    New_menu.show() 

    sys.exit(app.exec_())
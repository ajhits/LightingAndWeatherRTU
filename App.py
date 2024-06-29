from flask import Flask, render_template, Response,jsonify
from model.Object_detection import ObjectDetector

from firebase.ArduinoCom import Serial

import serial
import time
import cv2



app = Flask(__name__)

app.config["SERIAL_TIMEOUT"] = 1
app.config["SERIAL_PORT"] = "COM7"
app.config["SERIAL_BAUDRATE"] = 9600
    


# Create an instance of the ObjectDetector class
object_detector = ObjectDetector(model='model/ssd_mobilenet_v2.tflite')
object_detector.run()

ser = Serial(app)

# serial comunication
@app.route('/serial_IR', methods=['GET'])
def serial_IR():
    
    try:
        return jsonify("wait")
    except:
        return jsonify("0,0")

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

def generate_videofeed():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            continue
        
        try:
        
            # object detection
            frame = cv2.flip(frame, 1)
            frame = object_detector.detect_objects(frame)
        except Exception as e:
            pass
            print(e)
        
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Object detection   
@app.route('/video_feed')
def video_feed():
    return Response(generate_videofeed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        threaded=True,
        port=3000)
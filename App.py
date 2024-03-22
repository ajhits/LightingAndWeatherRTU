from flask import Flask, render_template, Response,jsonify
from model.Object_detection import ObjectDetector
from firebase.Firebase import Firebase

import cv2
import RPi.GPIO as GPIO
import time
import threading


DELAY_TIMEOUT = 1.5  # Equivalent to 1500 milliseconds

ir_right_pin = 20
ir_left_pin = 21

# in counter
in_counter = 0

# out counter
out_counter = 0

last_trigger_time = 0
is_walking_in = False
is_walking_out = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(ir_right_pin, GPIO.IN)
GPIO.setup(ir_left_pin, GPIO.IN)


app = Flask(__name__)

# in counter
app.config["in_counter"] = 0

# out counter
app.config["out_counter"] = 0


# Create an instance of the ObjectDetector class
object_detector = ObjectDetector(model='model/ssd_mobilenet_v2.tflite')
object_detector.run()

# ********************************* API ENDPOINTS

@app.route("/checkWalkIn", methods=["GET"])
def check_walk_in_api():
    global is_walking_in, last_trigger_time

    in_counter = app.config["in_counter"]
    
    ir_right_state = GPIO.input(ir_right_pin)

    if not is_walking_in and ir_right_state == GPIO.LOW:
        is_walking_in = True
        last_trigger_time = time.time()

    if time.time() - last_trigger_time > DELAY_TIMEOUT:
        is_walking_in = False

    ir_left_state = GPIO.input(ir_left_pin)
    if is_walking_in and ir_left_state == GPIO.LOW and ir_right_state == GPIO.HIGH:
        is_walking_in = False
        in_counter += 1
        last_trigger_time = time.time()
        
        Firebase().firebase_insert({
            "person_status": "person out",
            "last_trigger_time": last_trigger_time
        })
                
        print("Person entered. People in: {}, People out: {}".format(in_counter, out_counter))
        
    app.config["in_counter"] = in_counter

    # Prepare response data
    response_data = {
        "person_in":  app.config["in_counter"],
        "is_walking_in": is_walking_in,
        "last_trigger_time": last_trigger_time
    }
    
    print("walk in: ",response_data)
    return jsonify(response_data)

@app.route("/checkWalkOut", methods=["GET"])
def check_walk_out_api():
    global is_walking_out, last_trigger_time

    out_counter = app.config["out_counter"]
    in_counter = app.config["in_counter"]
    
    ir_left_state = GPIO.input(ir_left_pin)
        
    if not is_walking_out and ir_left_state == GPIO.LOW:
        is_walking_out = True
        last_trigger_time = time.time()
        
    if time.time() - last_trigger_time > DELAY_TIMEOUT:
        is_walking_out = False
        
    ir_right_state = GPIO.input(ir_right_pin)
    if is_walking_out and ir_right_state == GPIO.LOW and ir_left_state == GPIO.HIGH:
        is_walking_out = False
        out_counter += 1
        last_trigger_time = time.time()
        
        Firebase().firebase_insert({
            "person_status": "person out",
            "last_trigger_time": last_trigger_time
        })
            
        print("Person exited. People in: {}, People out: {}".format(in_counter, out_counter))
        if in_counter > 0:
            in_counter -= 1
            print("Person left the building. People in: {}, People out: {}".format(in_counter, out_counter))
        
    app.config["out_counter"] = out_counter
    app.config["in_counter"] = in_counter

    # Prepare response data
    response_data = {
        "person_out":  app.config["out_counter"],
        "is_walking_in": is_walking_in,
        "last_trigger_time": last_trigger_time
    }

    print("walk out: ",response_data)
    return jsonify(response_data)


# Homepage
@app.route('/')
def index():
    return render_template('index.html')

def generate_videofeed():
    cap = cv2.VideoCapture(0)
    frame_count = 0
    while True:
        success, frame = cap.read()
        if not success:
            continue
        
        # frame_count += 1
        # if frame_count % 2 == 0: 
        
        # object detection
        frame = cv2.flip(frame, 1)
        frame_with_objects = object_detector.detect_objects(frame)
        
        
        ret, jpeg = cv2.imencode('.jpg', frame_with_objects)
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
        port=3000)
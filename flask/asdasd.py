from flask import Flask, render_template, Response
from model.Object_detection import ObjectDetector
import cv2

app = Flask(__name__)

# Create an instance of the ObjectDetector class
object_detector = ObjectDetector(model='model/ssd_mobilenet_v2.tflite')
object_detector.run()

# @app.route('/')
# def index():
#     return render_template('index.html')


def generate_videofeed():
    cap = cv2.VideoCapture(1)
    frame_count = 0
    while True:
        success, frame = cap.read()
        if not success:
            continue
        
        # frame_count += 1
        # if frame_count % 2 == 0: 
            
        frame = cv2.flip(frame, 1)
        frame_with_objects = object_detector.detect_objects(frame)
        ret, jpeg = cv2.imencode('.jpg', frame_with_objects)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_videofeed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=3000)
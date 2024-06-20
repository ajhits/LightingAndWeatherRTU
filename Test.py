from flask import Flask, render_template, Response,jsonify
from SerialTest import Serial


app = Flask(__name__)
app.config["SERIAL_TIMEOUT"] = 1
app.config["SERIAL_PORT"] = "COM5"
app.config["SERIAL_BAUDRATE"] = 9600

ser = Serial(app)

# face recognition api | Time in  =========================================== #
@app.route('/test', methods=['GET'])
def face_recognition():
    data = ser.get_serial_message()

    print(data)
    return jsonify({ "data": data }),200

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        debug=True,
        threaded=True,
        port=3000)
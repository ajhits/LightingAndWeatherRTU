from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    
    # TYPE on raspberry Terminal: hostname -I
    # copy and replace the host
    app.run(
        host='0.0.0.0',
        debug=True,
        port=4000)
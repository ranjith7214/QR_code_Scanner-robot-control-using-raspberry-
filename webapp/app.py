import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask import request

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/left")
def left():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH

    GPIO.output(6, sig)
    GPIO.output(22, sig)
    
    return "OK"

@app.route("/forward")
def forward():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH

    GPIO.output(22, sig)
    GPIO.output(5, sig)
    return "OK"

@app.route("/backward")
def backward():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH

    GPIO.output(27, sig)
    GPIO.output(6, sig)
    return "OK"

@app.route("/right")
def right():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH

    GPIO.output(27, sig)
    GPIO.output(5, sig)
    
    return "OK"

if __name__ == "__main__":
    app.run(host='192.168.1.35', port=8000, debug=True)

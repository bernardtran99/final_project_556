import sys
import time
import threading
import subprocess
import os
import re
import json
import RPi.GPIO as GPIO
from datetime import datetime
from flask import *
from flask_socketio import SocketIO

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")

last_ring = 0
last_prox = 0
is_open = False
last_unlock = 0
app = Flask(__name__)

def get_last_ring():
    global last_ring
    return last_ring

def get_last_prox():
    global last_prox
    return last_prox

def get_state():
    global is_open
    return is_open

def get_unlock():
    global last_unlock
    return last_unlock

def push_callback(channel):
    global last_ring
    print("Update Ring")
    time.sleep(0.1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    last_ring = current_time

def prox_callback(channel):
    global last_prox
    print("Update Prox")
    time.sleep(0.1)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    last_prox = current_time

def unlock_door():
    global last_unlock
    print("Unlocking Door")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    last_unlock = current_time
    # put servo code here

def main_thread():
    global app
    app.run("0.0.0.0")

def sense_thread():
    global last_ring
    global last_prox
    global is_open
    # update sense info here
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(25, GPIO.RISING, callback = push_callback, bouncetime = 300)
    GPIO.add_event_detect(40, GPIO.RISING, callback = prox_callback, bouncetime = 300)
    GPIO.cleanup()

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('unlock') == 'Unlock Door':
            unlock_door()
            current_ring = get_last_ring()
            current_prox = get_last_prox()
            current_state = get_state()
            current_lock = get_unlock()
            return redirect(url_for("index"))
    current_ring = get_last_ring()
    current_prox = get_last_prox()
    current_state = get_state()
    current_lock = get_unlock()
    return render_template('content.html', current_ring = current_ring, current_prox = current_prox, current_state = current_state, current_lock = current_lock)

if __name__ == "__main__":
    t_main = threading.Thread(target = main_thread)
    t_sense = threading.Thread(target = sense_thread)
    t_main.start()
    t_sense.start()
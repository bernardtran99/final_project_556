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

def main_thread():
    global app
    app.run("0.0.0.0")

def sense_thread():
    global last_ring
    global last_prox
    global is_open

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

def unlock_door():
    global last_unlock
    print("Unlocking Door")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    last_unlock = current_time

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('unlock') == 'TRUE':
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
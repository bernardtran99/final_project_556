from asyncio import FastChildWatcher
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
open_num = 100

ring_ago = 0
prox_ago = 0
unlock_ago = 0
app = Flask(__name__)

GPIO_TRIGGER = 37
GPIO_ECHO = 33

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
    # send email

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
    # move servo

def main_thread():
    global app
    app.run("0.0.0.0")

def sense_thread():
    global last_ring
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(29, GPIO.RISING, callback = push_callback, bouncetime = 300)
    GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(40, GPIO.RISING, callback = prox_callback, bouncetime = 300)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def dist_thread():
    global is_open
    prev_num = 100
    open_before = False
    open_current = False
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    while True:
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)

        if dist <= 5:
            if open_current == False and open_before == False:
                is_open = "Yes"
                open_current = True
            if open_current == True and open_before == True:
                is_open = "No"
                open_current = False
        if dist > 5:
            if open_current == True:
                is_open = "Yes"
                open_before = True
            if open_current == False:
                is_open = "No"
                open_before = False
        # 3 states: door closed sensor = inf, door open sensor = inf, door open sensor < 5
        # if dist > 5 and prev_num > 5:
        #     # Door still close or still open"
        #     if open_before == False:
        #         #still closed
        #         is_open = "No"
        #     if open_current == True:
        #         #still open
        #         is_open = "Yes"
        # if dist < 5 and prev_num > 5:
        #     # "Door currently being opened or closed")
        #     if open_before == False:
        #         #currently being opened
        #         is_open = "Being Opened"
        #     if open_current == True:
        #         #currently being closed
        #         is_open = "Being Closed"
        # if dist < 5 and prev_num < 5:
        #     # print("Door currently blocking sensor fully")
        #     if open_before == False:
        time.sleep(1)

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
    t_dist = threading.Thread(target = dist_thread)
    t_main.start()
    t_sense.start()
    t_dist.start()
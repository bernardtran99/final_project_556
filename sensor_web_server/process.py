import sys
import time
import subprocess
import os
import re
import json 
from datetime import datetime
from flask import *
from flask_socketio import SocketIO

last_ring = 0
last_prox = 0
is_open = False

# def get_table():
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     network_list["TIME"] = current_time

#     result = subprocess.Popen(["sudo","iwlist","wlan0","scan"],stdout=subprocess.PIPE, universal_newlines=True)
#     output, error = result.communicate()

#     for line in output.split("\n"):

#         if re.search('Signal',line):
#             signal = re.search('Signal level=(.*) dBm',line)
#             signal_level = []
#             signal_level = signal.group(1)
        
#         if re.search('ESSID',line):
#             essid = re.search('ESSID:"(.*)"',line)
#             network_list[essid.group(1)] = signal_level
#             # print(essid.group(1))

#     return network_list

# app = Flask(__name__)

# @app.route("/")
# def index():
#     display_table = get_table()
#     return render_template('table.html', display_table=display_table)

def get_last_ring():
    global last_ring
    return last_ring

def get_last_prox():
    global last_prox
    return last_prox

def get_state():
    global is_open
    return is_open

app = Flask(__name__)

@app.route("/")
def index():
    current_ring = get_last_ring()
    current_prox = get_last_prox()
    current_state = get_state()
    return render_template('content.html', current_ring = current_ring, current_prox = current_prox, current_state = current_state)

if __name__ == "__main__":
    app.run("0.0.0.0")
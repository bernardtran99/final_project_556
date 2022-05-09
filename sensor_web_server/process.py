import sys
import time
import subprocess
import os
import re
from datetime import datetime
from flask import *

network_list = {}
display_table = {}

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

app = Flask(__name__)

@app.route("/")
def index():
    # display_table = get_table()
    # return render_template('table.html', display_table=display_table)
    return render_template('table.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
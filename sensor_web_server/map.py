#Bernard Tran

import sys
import time
import subprocess
import json
from flask import *
from flask_socketio import SocketIO

network_dict = {}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('content.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
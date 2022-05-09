import sys
import time
import subprocess
import os
import re
from datetime import datetime
from flask import *
import json
from flask_socketio import SocketIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('content.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
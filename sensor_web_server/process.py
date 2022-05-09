import sys
import time
import subprocess
import os
import re
import json
from datetime import datetime
from flask import *

# from flask_socketio import SocketIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('content.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
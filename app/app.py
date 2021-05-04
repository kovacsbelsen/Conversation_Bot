from pathlib import Path
from uuid import uuid4
import datetime as dt
import os
import requests
import sqlite3


from flask import Flask, jsonify, render_template, request

template_dir = Path("../templates")
app = Flask(__name__, template_folder=str(template_dir))

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def home():
    
    if request.method == "GET":
        return render_template("/index_speech.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():

    if request.method == "POST":
        mode = "deactivated"
        mode = request.form["mode"]
        r = requests.post("http://127.0.0.1:5003/predict", data=mode)
        
        r.raise_for_status()
        
        if r.json() == "deactivate":
            return render_template("/index_speech.html")
        


# FLASK_ENV=development FLASK_APP=app.py flask run --port=5002
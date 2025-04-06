# app/app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hallo Welt! Das Flask-Projekt läuft. 🎉"


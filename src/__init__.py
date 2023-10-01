from flask import Flask, render_template, request, send_file
import subprocess, secrets
import config

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe()
app.config.from_object(config.DevConfig)

from src import views

with app.app_context():
    if app.config["TESTING"]:
        print("\033[94mTesting mode detected.\033[0m")
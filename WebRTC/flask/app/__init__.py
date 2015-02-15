#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import Flask, session
from flask.sessions import SessionInterface
#from py.login import loginCtrl

# instancie une app
app = Flask(__name__)

from app import route

from flask import Flask
from flask import render_template
from py.login import loginForm
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask import Flask, session
from flask.sessions import SessionInterface

engine = create_engine('sqlite:///naheul.db')
session = Session(engine)

def login():
    form = loginForm.Login()
    name = form.name.data
    pwd = form.pwd.data
    values = form.data
    if form.validate_on_submit():
        print(name + pwd)
        print(values)
        for a in session.query(dbClass.Account):
        	if repr(a.login) == repr(name):
        		session[repr(a.login)]
    return render_template('login.html', form=form)
from flask import Flask, session
from flask import render_template
from py.login import loginForm
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)

def login():
    form = loginForm.Login()
    name = form.name.data
    pwd = form.pwd.data
    values = form.data
    if form.validate_on_submit():
        for a in dbSession.query(dbClass.Account):
        	if repr(a.login) == repr(name):
        		print(repr(a.login))
        		
    return render_template('login.html', form=form)
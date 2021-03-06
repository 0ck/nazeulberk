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
    session['login'] = ""
    if form.validate_on_submit():
        for a in dbSession.query(dbClass.Account):
            if repr(a.login) == repr(name):
                session['login'] = repr(a.login)
                message = 'vous etes connecte'
                return render_template('index.html', message=message)
    return render_template('login.html', form=form, login=session['login'])
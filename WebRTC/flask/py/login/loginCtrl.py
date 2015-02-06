from flask import Flask
from flask import render_template
from py.login import loginForm

def login():
    form = loginForm.Login()
    name = form.name.data
    pwd = form.pwd.data
    values = form.data
    if form.validate_on_submit():
        print(name + pwd)
        print(values)
    return render_template('login.html', form=form)
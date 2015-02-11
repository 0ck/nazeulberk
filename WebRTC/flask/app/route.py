from app import app
from flask import Flask, session
from flask import render_template
from py.login import loginCtrl
from py.zheros import zherosCtrl

@app.route("/room/<int:room_id>")
def enter_room(room_id):
    txt = render_template('room.html', room_id=room_id)
    print(txt)
    return txt

@app.route("/mj/<int:room_id>")
def enter_mj(room_id):
    txt = render_template('mj.html', room_id=room_id, login=session['login'])
    print(txt)
    return txt

@app.route("/joueur/<int:room_id>")
def enter_joueur(room_id):
    txt = render_template('joueur.html', room_id=room_id)
    print(txt)
    return txt

@app.route('/login/', methods=('GET', 'POST'))
def login():
    return loginCtrl.login()

@app.route('/zheros/', methods=('GET', 'POST'))
def zheros():
    return zherosCtrl.zheros()

@app.route("/")
def main():
    return render_template('index.html')
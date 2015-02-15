from app import app
from flask import Flask, session
from flask import render_template
from py.login import loginCtrl
from py.zheros import zherosCtrl
from py.createhero import createHeroCtrl
from py.hero import heroDetailCtrl
from py.roomClient import roomCtrl
from py.persoselect import persoSelectCtrl

@app.route("/perso/<int:id_perso>")
def setperso(id_perso):
    return persoSelectCtrl.set_session_perso(id_perso)

@app.route("/room/<int:room_id>")
def enter_room(room_id):
    return roomCtrl.room(room_id)

@app.route("/room/list/")
def room_list():
    txt = render_template('room_board.html')
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

@app.route("/hero/<int:hero_id>")
def hero_details(hero_id):
    return heroDetailCtrl.herodetails(hero_id)

@app.route('/login/', methods=('GET', 'POST'))
def login():
    return loginCtrl.login()

@app.route('/zheros/', methods=('GET', 'POST'))
def zheros():
    return zherosCtrl.zheros()

@app.route('/newhero/', methods=('GET', 'POST'))
def newhero():
    return createHeroCtrl.new()

@app.route("/")
def main():
    if session['login'] is None:
            session['login'] = ""
    return render_template('index.html')
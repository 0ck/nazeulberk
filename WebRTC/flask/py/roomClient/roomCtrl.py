from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)
print(repr(session))

def room(room_id):
	idPersoJoueur = str(session['perso'])
	persoJoueur = engine.execute('select * from Avatar where id = ' + idPersoJoueur).first()
	caracs = engine.execute('select * from Carac where id = ' + idPersoJoueur).first()
	print(persoJoueur)
	print(caracs)
	return render_template('room.html', room_id=room_id, persoJoueur=persoJoueur, caracs=caracs)
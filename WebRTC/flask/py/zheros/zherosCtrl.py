from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)
print(repr(session))

def zheros():
	if session['login'] is None:
		message = "Vous devez vous connecter pour acceder a cette page : zHeros"
		return render_template('index.html', message=message)
	elif session['login'] == "":
		message = "Vous devez vous connecter pour acceder a cette page : zHeros"
		return render_template('index.html', message=message)
	else:
	    for race in dbSession.query(dbClass.Race):
	        print(repr(race.name))
	    for metier in dbSession.query(dbClass.Metier):
	        print(repr(metier.name))
	    return render_template('zheros.html')
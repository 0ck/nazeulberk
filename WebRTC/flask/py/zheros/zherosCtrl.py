from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array
from py.zheros import getHero

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
		#login = str(session['login'])
		#User = engine.execute('select * from Account where login = ' + login).first()
		#idUser = str(User.id)
		#Persos = engine.execute('select * from Avatar where acc_id = ' + idUser)
		#for perso in Persos:
		#	idcarac = str(perso.carac_id)
		#	Caracs = engine.execute('select * from Carac where id = ' + idcarac).first()
		#	print(Caracs.COU)
		#	return render_template('zheros.html', perso=perso.name, caracs=Caracs)
		form = getHero.getHero()
		form.Avatar.choices = [(g.id, g.name) for g in dbSession.query(dbClass.Avatar).order_by('name')]
		return render_template('zheros.html', form=form)
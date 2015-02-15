from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)

def herodetails(hero_id):
	idp = str(hero_id)
	perso = engine.execute('select * from Avatar where id = ' + idp)
	caracs = engine.execute('select * from Carac where id = ' + idp).first()
	return render_template('herodetails.html', hero_id=hero_id, perso=perso, caracs=caracs)
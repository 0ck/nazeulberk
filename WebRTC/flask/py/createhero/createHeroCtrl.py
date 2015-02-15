from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array
from py.createhero import createHeroForm

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)
print(repr(session))

def new():
	form = createHeroForm.HeroCreate()
	form.Race.choices = [(g.id, g.name) for g in dbSession.query(dbClass.Race).order_by('name')]
	form.Metier.choices = [(g.id, g.name) for g in dbSession.query(dbClass.Metier).order_by('name')]
	return render_template('newhero.html', form=form)

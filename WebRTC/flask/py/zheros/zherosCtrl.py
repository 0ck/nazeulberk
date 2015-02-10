from flask import Flask, session
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)

def zheros():
    for race in dbSession.query(dbClass.Race):
        print(repr(race.name))
    for metier in dbSession.query(dbClass.Metier):
        print(repr(metier.name))
    return render_template('zheros.html')
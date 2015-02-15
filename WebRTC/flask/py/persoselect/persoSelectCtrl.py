from flask import Flask, session, redirect
from flask import render_template
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)
print(repr(session))

def set_session_perso(id_perso):
	session['perso'] = id_perso
	print(repr(session['perso']))
	return redirect('/room/list')
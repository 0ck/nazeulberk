from flask_wtf import Form
from wtforms import StringField
from wtforms import RadioField
from wtforms import SelectField
from wtforms.validators import DataRequired
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from array import array

engine = create_engine('sqlite:///naheul.db')
dbSession = Session(engine)

class getHero(Form):
#	ArrayClasse = {0:{}, 1:{}}
#	count = 0
#	for race in dbSession.query(dbClass.Race):
#		ArrayClasse[0][count] = {'name': race.name}
#		count = count + 1
#	count = 0
#	for metier in dbSession.query(dbClass.Metier):
#		ArrayClasse[1][count] = {'name': metier.name}
#		count = count + 1
	Avatar = SelectField(u'Avatar', coerce=int)
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

class HeroCreate(Form):
	Name = StringField('Pseudo', validators=[DataRequired()])
	Race = RadioField(u'Race', coerce=int)
	Metier = RadioField(u'Metier', coerce=int)
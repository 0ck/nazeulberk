from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class Login(Form):
    name = StringField('name', validators=[DataRequired()])
    pwd = StringField('pwd', validators=[DataRequired()])
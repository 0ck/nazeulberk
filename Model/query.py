#!/usr/bin/env python3

import model
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
session = Session(engine)

for a in session.query(model.Avatar):
    print(repr(a))

for a in session.query(model.Account):
    print(repr(a))

for a in session.query(model.Race):
    print(repr(a))

for a in session.query(model.Metier):
    print(repr(a))

for a in session.query(model.Carac):
    print(repr(a))

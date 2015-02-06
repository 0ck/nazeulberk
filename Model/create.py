#!/usr/bin/env python3

import hashlib
import model
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
model.Base.metadata.create_all(engine)

session = Session(engine)
session.add_all([
    model.Race(id=1, name='Humain'),
    model.Race(id=2, name='Barbare'),
    model.Race(id=3, name='Nain'),
    model.Race(id=4, name='Haut-Elfe'),
    model.Race(id=5, name='Demi-Elfe'),
    model.Race(id=6, name='Elfe Sylvain'),
    model.Race(id=7, name='Elfe Noir'),
    model.Race(id=8, name='Orque'),
    model.Race(id=9, name='Demi-Orque'),
    model.Race(id=10, name='Gobelin'),
    model.Race(id=11, name='Ogre'),
    model.Race(id=12, name='Semi-Homme'),
    model.Race(id=13, name='Gnome des forets du nord'),
    model.Metier(id=1, name='Guerrier'),
    model.Metier(id=2, name='Ninja'),
    model.Metier(id=3, name='Voleur'),
    model.Metier(id=4, name='Pretre'),
    model.Metier(id=5, name='Mage'),
    model.Metier(id=6, name='Paladin'),
    model.Metier(id=7, name='Ranger'),
    model.Metier(id=8, name='Menestrel'),
    model.Metier(id=9, name='Pirate'),
    model.Metier(id=10, name='Marchand'),
    model.Metier(id=11, name='Ingenieur'),
    model.Metier(id=12, name='Bourgeois'),
])
data = [
    model.Account(id=1, login='iopi', passwd=hashlib.sha224(b'1234').hexdigest(), email='lionel@lse.epita.fr'),
    model.Account(id=2, login='grudu', passwd=hashlib.sha224(b'/(&!!#').hexdigest(), email='lionel@lse.epita.fr'),
    model.Carac(id=1, COU=13, INT=12, CHA=9, AD=12, FO=13),
    model.Avatar(id=1, name='le nain', acc_id=1, metier_id=1, race_id=3, carac_id=1),
    model.Carac(id=2, COU=9, INT=13, CHA=11, AD=11, FO=11),
    model.Avatar(id=2, name='le ranger', acc_id=2, metier_id=7, race_id=1, carac_id=2),
    model.Carac(id=3, COU=11, INT=8, CHA=16, AD=11, FO=10),
    model.Avatar(id=3, name='l\'elf', acc_id=2, metier_id=1, race_id=6, carac_id=3),
]
session.add_all(data)
session.commit()


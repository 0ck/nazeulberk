#!/usr/bin/env python3

import hashlib
from py.model import dbClass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///naheul.db')
dbClass.Base.metadata.create_all(engine)

session = Session(engine)
session.add_all([
    dbClass.Race(id=1, name='Humain'),
    dbClass.Race(id=2, name='Barbare'),
    dbClass.Race(id=3, name='Nain'),
    dbClass.Race(id=4, name='Haut-Elfe'),
    dbClass.Race(id=5, name='Demi-Elfe'),
    dbClass.Race(id=6, name='Elfe Sylvain'),
    dbClass.Race(id=7, name='Elfe Noir'),
    dbClass.Race(id=8, name='Orque'),
    dbClass.Race(id=9, name='Demi-Orque'),
    dbClass.Race(id=10, name='Gobelin'),
    dbClass.Race(id=11, name='Ogre'),
    dbClass.Race(id=12, name='Semi-Homme'),
    dbClass.Race(id=13, name='Gnome des forets du nord'),
    dbClass.Metier(id=1, name='Guerrier'),
    dbClass.Metier(id=2, name='Ninja'),
    dbClass.Metier(id=3, name='Voleur'),
    dbClass.Metier(id=4, name='Pretre'),
    dbClass.Metier(id=5, name='Mage'),
    dbClass.Metier(id=6, name='Paladin'),
    dbClass.Metier(id=7, name='Ranger'),
    dbClass.Metier(id=8, name='Menestrel'),
    dbClass.Metier(id=9, name='Pirate'),
    dbClass.Metier(id=10, name='Marchand'),
    dbClass.Metier(id=11, name='Ingenieur'),
    dbClass.Metier(id=12, name='Bourgeois'),
])
data = [
    dbClass.Account(id=1, login='iopi', passwd=hashlib.sha224(b'1234').hexdigest(), email='lionel@lse.epita.fr'),
    dbClass.Account(id=2, login='grudu', passwd=hashlib.sha224(b'/(&!!#').hexdigest(), email='lionel@lse.epita.fr'),
    dbClass.Carac(id=1, COU=13, INT=12, CHA=9, AD=12, FO=13),
    dbClass.Avatar(id=1, name='le nain', acc_id=1, metier_id=1, race_id=3, carac_id=1),
    dbClass.Carac(id=2, COU=9, INT=13, CHA=11, AD=11, FO=11),
    dbClass.Avatar(id=2, name='le ranger', acc_id=2, metier_id=7, race_id=1, carac_id=2),
    dbClass.Carac(id=3, COU=11, INT=8, CHA=16, AD=11, FO=10),
    dbClass.Avatar(id=3, name='l\'elf', acc_id=2, metier_id=1, race_id=6, carac_id=3),
]
session.add_all(data)
session.commit()


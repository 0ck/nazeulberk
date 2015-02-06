from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'Account'

    id = Column(Integer, primary_key=True)
    login = Column(String(10))
    passwd = Column(String(56))
    email = Column(String(50))

    def __repr__(self):
        return 'Account(id={id}, login={login!r}, passwd={passwd!r}, email={email!r})'.format(**vars(self))

class Avatar(Base):
    __tablename__ = 'Avatar'

    id = Column(Integer, primary_key=True)
    # nom de l'aventurier
    name = Column(String(40))
    # niveau et experience
    level = Column(Integer)
    exp = Column(Integer)
    # caracteristique commune a toutes creatures
    carac_id = Column(Integer, ForeignKey('Carac.id'))
    # metier/race
    metier_id  = Column(Integer, ForeignKey('Metier.id'))
    race_id  = Column(Integer, ForeignKey('Race.id'))
    # correspond a un compte
    acc_id = Column(Integer, ForeignKey('Account.id'))

    def __repr__(self):
        return 'Avatar(id={id}, name={name!r}, acc_id={acc_id}, metier_id={metier_id}, race_id={race_id}, carac_id={carac_id})'.format(**vars(self))

class Metier(Base):
    __tablename__ = 'Metier'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    def __repr__(self):
        return 'Metier(id={id}, name={name!r})'.format(**vars(self))

class Race(Base):
    __tablename__ = 'Race'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    def __repr__(self):
        return 'Race(id={id}, name={name!r})'.format(**vars(self))

class Carac(Base):
    __tablename__ = 'Carac'

    # Caractéristique commune pour les joueurs ou les monstres

    id = Column(Integer, primary_key=True)
    # 5 caractéristiques de base
    COU = Column(Integer)
    INT = Column(Integer)
    CHA = Column(Integer)
    AD = Column(Integer)
    FO = Column(Integer)
    # point de vie max/courant
    PV_max = Column(Integer)
    PV = Column(Integer)
    # point de magie max/courant
    PM_max = Column(Integer)
    PM = Column(Integer)
    # Attaque/Parade
    AT = Column(Integer)
    PRD = Column(Integer)
    # plutot pour les joueurs ou les gros PNJ
    PointDestin = Column(Integer)
    # Piece d'or Porté
    PO = Column(Integer)

    def __repr__(self):
        return ('Carac(id={id}, COU={COU}, INT={INT}, CHA={CHA}, AD={AD}, FO={FO},\n'
                + ' PV={PV}/{PV_max}, PM={PM}/{PM_max}, AT={AT}, PRD={PRD}, PO={PO}, PdD={PointDestin})'
        ).format(**vars(self))

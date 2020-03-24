from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


user_serv = db.Table('user_serv',
    db.Column('utilisateurs_id', db.Integer, db.ForeignKey('utilisateurs.id')),
    db.Column('serveurs_id', db.Integer, db.ForeignKey('serveurs.id')),
)

class Utilisateurs(db.Model):
    __tablename__ = 'utilisateurs'
    id=db.Column(db.Integer, primary_key=True)
    uid=db.Column(db.String(10),unique=True)
    nom=db.Column(db.Text,nullable=False)
    prenom=db.Column(db.Text,nullable=False)
    classe=db.Column(db.Text,nullable=False)
    groupe=db.Column(db.String(10))
    machines_Virtuelles = db.relationship('Machines_Virtuelles', backref='utilisateurs', lazy=True)
    serveurs = db.relationship('Serveurs', viewonly=True, secondary=user_serv, lazy='subquery',backref=db.backref('utilisateurs', lazy=True))

class Serveurs(db.Model):
    __tablename__ = 'serveurs'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(30),nullable=False)
    machines_Virtuelles = db.relationship('Machines_Virtuelles', backref='serveurs', lazy=True)

class Machines_Virtuelles(db.Model): 
    __tablename__ = 'machines_virtuelles'
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(30),nullable=False)
    adresse_IP=db.Column(db.String(15),nullable=False) # taille @IP 15 en askii masque non compté
    adresse_MAC=db.Column(db.String(17),nullable=False)
    port_RDP=db.Column(db.String(5),nullable=False)
    commentaire=db.Column(db.Text)
    utilisateurs_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'),nullable=False)
    serveur_id = db.Column(db.Integer, db.ForeignKey('serveurs.id'),nullable=False)
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from tabledef import *

db.create_all()

x = Utilisateurs(id='1',uid='aimeadr',nom='Aimé',prenom='Adrian',classe='M1TRI',groupe='2')
y = Utilisateurs(id='2',uid='alsawaha',nom='Al Sawah',prenom='Ahmed',classe='M1TRI',groupe='1') 
z = Utilisateurs(id='3',uid='badair',nom='Badai',prenom='Ryan',classe='L3TRI',groupe='1') 

a = Serveurs(id='1',nom='mau-59-serv14')
b = Serveurs(id='2',nom='mau-59-serv15')
c = Serveurs(id='3',nom='mau-59-serv16')
d = Serveurs(id='4',nom='mau-59-serv17')

x.serveurs.append(a)
x.serveurs.append(d)
x.serveurs.append(a)
y.serveurs.append(b)
z.serveurs.append(a)

m = Machines_Virtuelles(id='1',nom='mau-59-aimeadr',adresse_IP='192.168.176.201',adresse_MAC='08:00:27:01:FE:00',port_RDP='3389',commentaire='Vm de adrian')
n = Machines_Virtuelles(id='2',nom='mau-59-alsawah',adresse_IP='192.168.176.202',adresse_MAC='08:00:27:01:FE:01',port_RDP='3389',commentaire='Vm de ahmed')
o = Machines_Virtuelles(id='3',nom='mau-59-badair',adresse_IP='192.168.176.203',adresse_MAC='08:00:27:01:FE:02',port_RDP='3390',commentaire='Vm de ryan')

x.machines_Virtuelles.append(m)
y.machines_Virtuelles.append(n)
z.machines_Virtuelles.append(o)

a.machines_Virtuelles.append(m)
a.machines_Virtuelles.append(o)
b.machines_Virtuelles.append(n)

db.session.add_all([x,y,z,a,b,c,d,m,n,o])

db.session.commit()

# Utilisateurs.query.all()
# ad = Utilisateurs.query.filter_by(nom='Aimé').first()
# >>> ad.serveurs
# [<Serveurs 1>, <Serveurs 4>]
# >>> ad.serveurs[0].nom
# 'mau-59-serv14'

# >>> ad.machines_Virtuelles[0].nom
# 'mau-59-aimeadr'
# >>> ad.machines_Virtuelles[0].adresse_IP
# '192.168.176.201'

# >>> se = Serveurs.query.first()
# >>> se.nom
# 'mau-59-serv14'
# >>> se.utilisateurs
# [<Utilisateurs 1>, <Utilisateurs 3>]
# >>> se.utilisateurs[0].nom
# 'Aimé'

# >>> se.machines_Virtuelles[0].nom
# 'mau-59-aimeadr'
# >>> se.machines_Virtuelles[1].nom
# 'mau-59-badair'


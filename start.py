from flask import Flask, render_template, request,redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from tabledef import *
from scripts.conf import *
from scripts.recuperation_utilisateur import *

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    users=Utilisateurs.query.all()
    return render_template('index.html',users=users)
@app.route('/test', methods=['GET'])
def index2():
    # vms=Machines_Virtuelles.query.all()
    users=Utilisateurs.query.all()
    return render_template('index2.html',users=users)

@app.route('/config', methods=["GET", "POST"])
def config():
    data = None
    c = Conf('config/app.conf')
    b = c.testError()
    if(b):
        data = "Erreur"
    else:
        data = c.readAll()

    return render_template('config.html', data=data)

@app.route('/traitconf', methods=['GET', 'POST'])
def traitconf():
    c = Conf('config/app.conf')
    if request.method == 'POST':
        print("POST")
        for o in request.form:
            section = o.split('.')[0]
            option = o.split('.')[1]
            value = request.form[o]
            c.addOption(section, option, value)
        return redirect(url_for('config'))

@app.route('/admin', methods=["GET", "POST"])
def admin():
    data = None
    c = Conf('config/app.conf')
    b = c.testError()
    if(b):
        data = "Erreur"
    else:
        data = c.readSection("ldap")

    return render_template('admin.html', data=data)

@app.route('/add_users', methods=['GET','POST'])
def add_users():
    if request.method == 'POST':
        c = Conf('config/app.conf')
        result = request.form
        ls=Recuperation_utilisateur("scripts/doc.xlsx","etudiants-m1-sts-rt-tri",c.readOption("LDAP","serveur_ldap"),c.readOption("LDAP","utilisateur_ldap"),result['pwd'])
        print(ls)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


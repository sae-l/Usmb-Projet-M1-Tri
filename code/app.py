from flask import Flask, render_template, request,redirect, url_for, flash, request,session,send_from_directory,abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,login_required,UserMixin,login_user,logout_user,current_user
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import TextField,PasswordField,validators
from wtforms.validators import InputRequired,DataRequired
from db import *
from scripts.conf import *
from scripts.recuperation_utilisateur import *
from scripts.attribution_vm import *
from scripts.repartition import *
from scripts.playbook import *
from scripts.ssh import *
import locale
import ldap,string
import json
import requests 
import hashlib

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)
login_manager.session_protection = "strong"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY=True

"""
****                    *             
*   *                   *             
*   *                   *             
*   *   ****   *    *  ****    ****   
****   *    *  *    *   *     *    *  
**     *    *  *    *   *     ******  
* *    *    *  *    *   *     *       
*  *   *    *  *   **   *  *  *    *  
*   *   ****    *** *    **    ****  
"""
@app.route('/', methods=['GET'])
def index():
#Fonction d'affichage pour la route par défaut
    form = LoginForm()
    users=Utilisateurs.query.all()
    return render_template('index.html',users=users, form=form)


@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html')

@app.route('/configuration', methods=["GET"])
@login_required
def config():
#Fonction d'affichage pour la page de configuration
    form = LoginForm()
    data = None
    c = Conf('config/app.conf')
    b = c.testError()
    serveurs = Serveurs.query.all()
    groupes=c.readSection("GROUPES")
    if(b):
        data = "Erreur"
    else:
        data = c.readAll()


    return render_template('configuration.html', data=data,groupes=groupes,serveurs=serveurs,form=form)

#Fonction d'affichage de la page 
#Methode POST utile car retour de la page d'ajouts de plusieurs utilisateurs
@app.route('/creation_utilisateurs', methods=["GET", "POST"])
@login_required
def creation_utilisateurs():
    form = LoginForm()
    data = None #ldap
    data2 = None #groupes
    c = Conf('config/app.conf')
    b = c.testError()
    if(b):
        data = "Erreur"
        data2 = "Erreur"
    else:
        data = c.readSection("AUTHENTIFICATION")
        data2 = c.readSection("groupes")

    return render_template('creation_utilisateurs.html', data=data, data2=data2, form=form)

#Fonction de retour pour le lancement des scripts 
#et renvoi sur la page de confirmation

@app.route('/ajouter_utilisateurs', methods=['GET','POST'])
@login_required
def ajouter_utilisateurs():
    form = LoginForm()
    if request.method == 'POST':
        c = Conf('config/app.conf')
        result = request.form
        password = result['pwd']
        files = request.files
        result = []

        #Tableau contenant les données a envoyer a la page
        inLdap = []
        inExcel = []
        inLesDeux = []

        for f in files:
            if request.files[f]:
                #Récupération des données dans les fichiers Excel + Récupération des données du LDAP
                arr = []
                fakeArr = []
                fi = request.files[f]
                path = app.config["MEDIA"] + f + ".xlsx"
                server = c.readOption("AUTHENTIFICATION","serveur_ldap")
                #print(current_user.id)
                fi.save(path)
                ldapUser = session.get('username')
                #Fusion des 2 listes
                ls=Recuperation_utilisateur(path,f,server,ldapUser,password)

                #Création de 3 tableaux, 1 pour etudiant présent que dans le LDAP, 1 pour etudiant présent que dans Excel, et un dernier pour ceux présent partout
                #Si un etudiant n'a pas de UID, il n'est que dans Excel
                #Si un etudiant n'a pas de groupen il n'est que dans le LDAP
                #Le reste est dans les 2

                inLdapt = []
                inExcelt = []
                inLesDeuxt = []

                fakeArr.append(f)

                inLdapt.append(fakeArr)
                inExcelt.append(fakeArr)
                inLesDeuxt.append(fakeArr)
                for etu in ls:
                    if etu[0] == '':
                        #print('dans excel')
                        inExcelt.append(etu)
                    elif etu[3] == '':
                        #print('dans ldap')
                        inLdapt.append(etu)
                    else:
                        #print('dans les 2')
                        inLesDeuxt.append(etu)
                inLdap.append(inLdapt)
                inExcel.append(inExcelt)
                inLesDeux.append(inLesDeuxt)

    # print(inLdap)

    return render_template('adduser.html', inLdap=inLdap, inExcel=inExcel, inLesDeux=inLesDeux, form=form)

@app.route('/ajout_utilisateurs_bdd', methods=['GET','POST'])
def ajout_utilisateurs_bdd():
    form = LoginForm()
    if request.method == 'POST':

        result = request.form
        user = result['user']
        password = result['password']
        #Groupe contenant les étudiants
        arrEtudiants = []
        arrGroupes = []
        arrSuppression = []
        #print(result)
        #print("_____")
        #for liste in result:
        liste = result['data']
        #print(liste)
        #print("_-_-_-_-_-_")
        etudiants = json.loads(liste)
        for etudiant in etudiants:
            userBDD = Utilisateurs.query.filter_by(uid=etudiant[0]).first()
            # print(userBDD)
            #Si user dans la base, mise a jour des infos (groupe et classe)
            if userBDD:
                #print(userBDD)
                userBDD.classe = etudiant[4]
                userBDD.groupe = etudiant[3]
                db.session.commit()
            #Si user pas dans la base, creation de l'user dans la base
            else:
                user=Utilisateurs(uid=etudiant[0],nom=etudiant[1],prenom=etudiant[2],classe=etudiant[4],groupe=etudiant[3])
                db.session.add(user)
                db.session.commit()
                serveur=serveur_un_utilisateur(liste_server())
                attribution=attribution_vms(serveur,etudiant[0], user, password)
                db.session.commit()

            arrEtudiants.append(etudiant[0])
            if etudiant[4] not in arrGroupes:
                arrGroupes.append(etudiant[4])

    for grp in arrGroupes:
        r = Utilisateurs.query.with_entities(Utilisateurs.uid).filter_by(classe=grp).all()
        for etu in r:
            if etu[0] not in arrEtudiants and etu[0] not in arrSuppression:
                deletedEtu = Utilisateurs.query.with_entities(Utilisateurs.uid, Utilisateurs.nom, Utilisateurs.prenom, Utilisateurs.groupe, Utilisateurs.classe).filter_by(uid=etu[0]).first()
                arrSuppression.append(deletedEtu)
    #print("suppression")
    #print(arrSuppression)

    return render_template('valider_supprimer_utilisateurs.html',users=arrSuppression, form=form)

@app.route('/suppression_utilisateurs_bdd', methods=['GET','POST'])
def suppression_utilisateurs_bdd():
    form = LoginForm()
    if request.method == 'POST':
        result = request.form
        #Lecture du json envoyé
        arrSuppression = json.loads(result['data'])
        uid_suppr=[]
        #Suppression de sutilisatuer
        #Il faut supprimer les VM des utilisateurs avant de supprimer les utilisateurs
        # print(arrSuppression)
        for etu in arrSuppression:
            # print(etu)
            userBDDDelete = Utilisateurs.query.filter_by(uid=etu[0]).first()
            uid_suppr.append(etu[0])
            for vm in userBDDDelete.machines_Virtuelles:
                db.session.delete(vm)
                db.session.commit()
            userBDDDelete.serveurs.clear()
            db.session.delete(userBDDDelete)
            db.session.commit()
        if result['removeDossier']==True:
            suppresion_dossier_serveurs(uid_suppr)
    return redirect(url_for('creation_utilisateurs'))


#Fonction d'affichage de la page
@app.route('/administration_utilisateurs', methods=['GET'])
@login_required
def admin_user():
    form = LoginForm()
    c = Conf('config/app.conf')
    users=Utilisateurs.query.all()
    groupes = c.readSection("GROUPES")
    return render_template('administration_utilisateurs.html',users=users,groupes=groupes, form=form)

@app.route('/administration_vms', methods=['GET'])
@login_required
def admin_vms():
    form = LoginForm()
    users=Utilisateurs.query.all()
    return render_template('administration_vms.html',users=users, form=form)

"""
*                                     
*                        *            
*                                     
*       ****    *** *   **    * ***   
*      *    *  *   *     *    **   *  
*      *    *  *   *     *    *    *  
*      *    *   ***      *    *    *  
*      *    *  *         *    *    *  
*****   ****    ****   *****  *    *  
               *    *                 
                ****                  
"""

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    c = Conf('config/app.conf')
    uid_auth = c.readOption("AUTHENTIFICATION","uid_authorise")
    users=uid_auth.split(',')
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    c = Conf('config/app.conf')
    uid_auth = c.readOption("AUTHENTIFICATION","uid_authorise")
    users=uid_auth.split(',')
    if username not in users:
        return

    user = User()
    return user

class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
# Fonction pour se connecter
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html',form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            c = Conf('config/app.conf')
            username = request.form['username']
            password = request.form['password']

            # Connection via compte root
            if username=='root':
                mdp_Root = c.readOption("AUTHENTIFICATION","mot_de_passe_root")
                passwd, salt = mdp_Root.split(':')
                if passwd == hashlib.sha256(salt.encode() + password.encode()).hexdigest():
                    session['username'] = username
                    user = User()
                    user.id = username
                    login_user(user)
            else:
                adresse = c.readOption("AUTHENTIFICATION","serveur_ldap")
                try:
                    connection=ldap.initialize("ldaps://%s:636"%(adresse), bytes_mode=False)
                    connection.simple_bind_s("uid=%s,ou=people,ou=uds,dc=agalan,dc=org"%(username), "%s"%(password))
                except ldap.INVALID_CREDENTIALS:
                    return redirect(url_for('index'))
                session['username'] = username
                user = User()
                user.id = username
                login_user(user)
            
            return redirect(url_for('index'))

    return 'Bad login'

# fonction de deconnection
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))
    
"""
*   *           
*   *           
*   *           
 * *   * * **   
 * *   ** *  *  
 * *   *  *  *  
  *    *  *  *  
  *    *  *  *  
  *    *  *  *  

"""
#Fonction de retour pour le l'attribution de vm
#et renvoi sur la page de confirmation
@app.route('/ajouter_vm', methods=['POST'])
@login_required
def add_vms():
    #TODO debug
    user = "user"
    password = "password"

    form = LoginForm()
    if request.method == 'POST':
        result = request.form
        # On choisi un serveur
        serveur=serveur_un_utilisateur(liste_server())
        servers = Serveurs.query.all()
        servs=[]
        for s in servers:
            servs.append(s.nom)
        nom = attribution_vms(serveur,result['uid'], user, password)
        # machine = Machines_Virtuelles(nom=attribution[0],adresse_IP=attribution[1],adresse_MAC=attribution[3],port_RDP=attribution[4],commentaire='Vm de '+attribution[5])
        vm=Machines_Virtuelles.query.filter_by(nom=nom).first()
        return render_template('mod_vm.html',servs=servs,vm=vm,form=form)

# Fonction qui creer un dictonaire de serveur avec les nombre de vm qu'ils heberge en valeur
def liste_server():
    liste={}
    serveur = Serveurs.query.all()
    for serv in serveur:
        liste[serv.nom]=len(serv.machines_Virtuelles)
    return liste

#Fonction de lancement de script pour l'attribution des vms
def attribution_vms(serveur,uid, user, password):
    c = Conf('config/app.conf')
    liste_rdp=[]
    ip_used=[]
    mac_used=[]

    # defini le nom de vm à utiliser
    user=Utilisateurs.query.filter_by(uid=uid).first()
    nom_user=user.prenom
    if len(user.machines_Virtuelles)==0:
        nom='mau-59-'+uid+'-0'
    else:
        nb=0
        tab_num=[]
        for vm in user.machines_Virtuelles:
            num=vm.nom.split("-")
            tab_num.append(int(num[3]))
        nom='mau-59-'+uid+'-'+str(max(tab_num)+1)

    # On creer les liste des adresse/port deja pourvu

    vm_RDP=Serveurs.query.filter_by(nom=serveur).first()
    for vm in range(0,len(vm_RDP.machines_Virtuelles)):
        liste_rdp.append(vm_RDP.machines_Virtuelles[vm].port_RDP)

    vms=Machines_Virtuelles.query.all()
    for vm in vms:
        ip_used.append(vm.adresse_IP)
        mac_used.append(vm.adresse_MAC)

    vma=attribution_vm(c.readOption("IP","plage_ip"),ip_used,liste_rdp,c.readOption("RDP","port_rdp_debut"),c.readOption("RDP","port_rdp_fin"),c.readOption("MAC","plage_mac_debut"),c.readOption("MAC","plage_mac_fin"),mac_used)
    
    # Creation du commentaire
    comm = 'Vm de '+nom_user
    machine = Machines_Virtuelles(nom=nom,adresse_IP=vma[0],adresse_MAC=vma[1],port_RDP=vma[2],commentaire=comm)

    #reservation_base_machine(vma[0], vma[1], nom, comm, user, password)

    serveur = Serveurs.query.filter_by(nom=serveur).first()
    utilisateur = Utilisateurs.query.filter_by(uid=uid).first()

    # On la relie aux autres tables
    utilisateur.serveurs.append(serveur)
    utilisateur.machines_Virtuelles.append(machine)
    serveur.machines_Virtuelles.append(machine)

    db.session.add_all([utilisateur,serveur,machine])
    db.session.commit()
    creation_playbook()

    return machine.nom

#Fonction qui envoie sur la page pour modifier une vm    
@app.route('/modifier_vm', methods=['POST'])
@login_required
def mod_vm():
    form = LoginForm()
    if request.method == 'POST':
        servers = Serveurs.query.all()
        servs=[]
        for s in servers:
            servs.append(s.nom)
        result = request.form
        vm=Machines_Virtuelles.query.filter_by(nom=result['nom']).first()
        return render_template('mod_vm.html',servs=servs,vm=vm,form=form)

#Fonction de retour pour la modication de vm    
@app.route('/modification_vm', methods=['POST'])
@login_required
def modi_vm():
    if request.method == 'POST':
        result = request.form
        vm=Machines_Virtuelles.query.filter_by(id=result['id']).first()
        user=result['user']
        password=result['password']
        #On supprime la VM, puis on en créé une. (Pour la modifier)
        #reservation_base_machine(vm.adresse_IP, vm.adresse_MAC, vm.nom, "A Supprimer", user, password)
        vm.nom=result['nom']
        vm.adresse_MAC=result['mac']
        vm.adresse_IP=result['ip']
        vm.port_RDP=result['rdp']
        vm.commentaire=result['com']
        db.session.commit()
        #reservation_base_machine(vm.adresse_IP, vm.adresse_MAC, vm.nom, vm.commmentaire, user, password)
        creation_playbook()
        return redirect(url_for('index')) 


#Fonction de retour pour supprimer une vm    
@app.route('/supprimer_vm', methods=['POST'])
@login_required
def del_vms():
    if request.method == 'POST':
        result = request.form
        vm=Machines_Virtuelles.query.filter_by(nom=result['nom']).first()
        user=result['user']
        password=result['password']
        #Signature : reservation_base_machine(ip, mac, nom, commentaire, user, password)
        #reservation_base_machine(vm.adresse_IP, vm.adresse_MAC, vm.nom, "A Supprimer", user, password)
        db.session.delete(vm)
        db.session.commit()
        creation_playbook()
        return redirect(url_for('admin_vms'))

#Fonction de réservation des données dans base machine
#Recupere l'URL dans le fichier de configuration
def reservation_base_machine(ip, mac, nom, commentaire, user, password):
    c = Conf('config/app.conf')
    adresse = c.readOption("CONFIGURATION_GENERALE",'adresse_base_machine')
    data = {'IPAddress':ip, 'MacAddress':mac, 'MName':nom, 'Comment':commentaire}
    r = requests.post(url = adresse, data = data, auth = (user, password))

#genere le playbook ansible a partir de la bdd
def creation_playbook():
    server = Serveurs.query.all()
    result=[]
    for serveur in server:
        usertab=[]
        for vm in serveur.machines_Virtuelles:
            usertab.append(vm.utilisateurs.uid)
        result.append((serveur.nom,usertab))
    createPlaybook(result)

# fonction qui cherche les options puis appelle le script pour supprimer les dossier sur le serveur
def suppresion_dossier_serveurs(uid):
    c = Conf('config/app.conf')
    servs=Serveurs.query.all()
    serveurs=[]
    for serv in servs:
        serveurs.append(serv.nom+".local.univ-savoie.fr")
    ssh_suppr_folder(serveurs,c.readOption("CONFIGURATION_GENERALE","location_clef"),c.readOption("CONFIGURATION_GENERALE","chemin_location_vm"),uid)
"""
*   *                        
*   *                        
*   *                        
*   *   ****    ****   * **  
*   *  *    *  *    *   *    
*   *   **     ******   *    
*   *     **   *        *    
*   *  *    *  *    *   *    
 ***    ****    ****    *  
"""

#Fonction de retour pour ajouter un utilisateur
@app.route('/ajouter_utilisateur', methods=['POST'])
@login_required
def ajt_user():
    if request.method == 'POST':
        result = request.form
        user=Utilisateurs(uid=result['inputUid'],nom=result['inputName'],prenom=result['inputFirstname'],classe=result['inputClasse'],groupe=result['inputGroupe'])
        db.session.add(user)
        db.session.commit()
        serveur=serveur_un_utilisateur(liste_server())
        nom = attribution_vms(serveur,result['inputUid'], result['user'], result['password'])
        vm=Machines_Virtuelles.query.filter_by(nom=nom).first()
        return redirect(url_for('admin_user'))

#Fonction de retour pour supprimer un utilisateur
@app.route('/supprimer_utilisateur', methods=['POST'])
@login_required
def del_user():
    if request.method == 'POST':
        result = request.form
        print(result)
        for key,val in result.items():
            if key!="csrf_token":
                if key!="removeDossier":
                    user=Utilisateurs.query.filter_by(uid=val).first()
                    # On supprime les vm de l'utilisateur
                    for vm in user.machines_Virtuelles:
                        db.session.delete(vm)
                        db.session.commit()
                    # On supprime l'utilisateur du tableau n:n puis sa table
                    user.serveurs.clear()
                    db.session.delete(user)
                    db.session.commit()
                    # On met met a jour le playbook
                    creation_playbook()
                    # On supprime les dossier sur les serveurs
                    
                    if ('removeDossier'in result) and (result['removeDossier']=='True'):
                        suppresion_dossier_serveurs(val)
        return redirect(url_for('admin_user')) 

"""
 ***                     ***                  
*   *                   *   *    *            
*                       *                     
*       ****   * ***    *       **     *** *  
*      *    *  **   *  ****      *    *   *   
*      *    *  *    *   *        *    *   *   
*      *    *  *    *   *        *     ***    
*   *  *    *  *    *   *        *    *       
 ***    ****   *    *   *      *****   ****   
                                      *    *  
                                       **** 
"""
#Fonction de retour pour le changements de configuration
#modifie les configuration dans le fichier
@app.route('/traitconf', methods=['POST'])
@login_required
def traitconf():
    c = Conf('config/app.conf')
    if request.method == 'POST':
        for o in request.form:
            if o!="csrf_token":
                section = o.split('.')[0]
                option = o.split('.')[1]
                value = request.form[o]
                if option=='mot_de_passe_root':
                    c.addOptionHash(section, option, value)
                else:
                    c.addOption(section, option, value)
        return redirect(url_for('config'))

#Fonction de retour pour l'ajout de groupe
@app.route('/ajouter_groupe', methods=['POST'])
def ajouter_groupe():
    c = Conf('config/app.conf')
    liste_groupe=[]
    if request.method == 'POST':
        liste_tuple_groupe=c.readSection("GROUPES")
        for tuple_groupe in liste_tuple_groupe:
            liste_groupe.append(tuple_groupe[0])
        max_groupe = max(liste_groupe)
        c.addOption("GROUPES",max_groupe[:-1] + chr(ord(max_groupe[-1]) + 1),"null")
    return redirect(url_for('config'))

#Fonction de retour pour la suppresion d'un groupe
@app.route('/supprimer_groupe', methods=['POST'])
def supprimer_groupe():
    c = Conf('config/app.conf')
    if request.method == 'POST':
        result = request.form
        c.deleteOption("GROUPES",result["Radios"])
    return redirect(url_for('config'))

#Fonction de retour pour l'ajout d'un serveur
@app.route('/ajouter_serveur', methods=['POST'])
def ajouter_serveur():
    if request.method == 'POST':
        result = request.form
        serv=Serveurs(nom=result["nom_serveur"])
        db.session.add(serv)
        db.session.commit()
    return redirect(url_for('config'))

#Fonction de retour pour la suppression d'un serveur
@app.route('/supprimer_serveur', methods=['POST'])
def supprimer_serveur():
    if request.method == 'POST':
        result = request.form
        serv=Serveurs.query.filter_by(id=result["Radios"]).first()
        # On supprime les vm associé au serveur
        for vm in serv.machines_Virtuelles:
            db.session.delete(vm)
        db.session.delete(serv)
        db.session.commit()
    return redirect(url_for('config'))

# Fonction utilisé pour authorisé en lancer le téléchargement du playbook ansible
@app.route("/public/playbook")
def download_playbook():
    try:
        return send_from_directory(app.config["PUBLIC"], "playbook.yml", as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request,redirect, url_for, flash, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,login_required,UserMixin,login_user,logout_user,current_user
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import TextField,PasswordField,validators
from wtforms.validators import InputRequired,DataRequired
from tabledef import *
from scripts.conf import *
from scripts.recuperation_utilisateur import *
from scripts.attribution_vm import *
from scripts.repartition import *
import locale
import ldap,string
import json
import requests 
import hashlib

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
# csrf = CSRFProtect(app)
login_manager.session_protection = "strong"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY=True

media = "media/"

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
@app.route('/creation_utilisateurs', methods=["GET"])
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

        for f in files:
            arr = []
            fi = request.files[f]
            path = media + f + ".xlsx"
            server = c.readOption("AUTHENTIFICATION","serveur_ldap")
            # TODO Recuperer le mdp enregistreé
            #print(current_user.id)
            fi.save(path)
            ls=Recuperation_utilisateur(path,f,server,ldapUser,password)
            arr.append(f)
            arr.append(ls)
            result.append(arr)



#     return render_template('adduser.html', data=result)

    #return render_template('adduser.html', data=[['etudiants-l3-sts-sc-et-techno-tri', [['badair', 'Badai', 'Ryan', ''], ['cauetb', 'Cauet', 'Baptiste', ''], ['duvalc', 'Petit', 'Cyprien', ''], ['goumaa', 'Gouma', 'Archange', ''], ['ladetj', 'Ladet', 'Julien', ''], ['longjo', 'Long', 'Joris', ''], ['niazih', 'Niazi', 'Hazrat-Bilal', ''], ['ribotm', 'Ribot', 'Maude', ''], ['tallfa', 'Tall', 'Fatou', ''], ['blancad', 'Blanc', 'Adrien', ''], ['boisced', 'Bois', 'Cedric', ''], ['camposc', 'Campos', 'Celian', ''], ['feutryh', 'Feutry', 'Hugo', ''], ['guissep', 'Guisse', 'Papa-Mouhamadou', ''], ['idelont', 'Idelon', 'Teo', ''], ['kociolt', 'Kociol', 'Thomas', ''], ['redontg', 'Redont', 'Gaspard', ''], ['boissiel', 'Boissier', 'Lucas', ''], ['boubousa', 'Legrand', 'Samuel', ''], ['bouvierp', 'Bouvier', 'Pierre', ''], ['cathelib', 'Cathelineau', 'Benjamin', ''], ['chatejul', 'Chatel', 'Julien', ''], ['durajean', 'Durand', 'Jean', ''], ['janosevd', 'Janosevic', 'Damien', ''], ['jondeauk', 'Jondeau', 'Kassim', ''], ['laurmaxe', 'Laurent', 'Maxence', ''], ['maghakia', 'Maghakian', 'Alex', ''], ['mahamara', 'Mahaman-Moussa', 'Rahamatou', ''], ['ortegalu', 'Ortega', 'Ludovic', ''], ['philippd', 'Philippe', 'Damien', ''], ['raffelet', 'Raffele', 'Thomas', ''], ['rochejoa', 'Rocher', 'Joachim', ''], ['tournour', 'Tournoud', 'Remi', ''], ['trouvean', 'Trouve', 'Antoine', ''], ['', 'Aime', 'Adrian', 2], ['', 'Al-Sawah', 'Ahmed', 1], ['', 'fcwc', 'cwwc', 4]]], ['etudiants-m1-sts-rt-tri', [['jammet', 'Jamme', 'Thomas', ''], ['simria', 'Simri', 'Anas', ''], ['aimeadr', 'Aime', 'Adrian', 2], ['ginardv', 'Ginard', 'Valentin', ''], ['janinda', 'Janin', 'Damien', ''], ['sauzera', 'Sauzer', 'Antoine', ''], ['wangyij', 'Wang', 'Yijie', ''], ['yasarmi', 'Yasar', 'Mikail', ''], ['alsawaha', 'Al-Sawah', 'Ahmed', 1], ['bachnouz', 'Bachnou', 'Zahir', ''], ['brassoux', 'Brassoud', 'Xavier', ''], ['cecillre', 'Cecillon', 'Remi', ''], ['constann', 'Constandi', 'Nicolas', ''], ['davithib', 'David', 'Thibaut', ''], ['duboisma', 'Dubois', 'Marc', ''], ['hoffmanb', 'Hoffmann', 'Baptiste', ''], ['idrissah', 'Idrissa', 'Hilda-Binti', ''], ['jacqueax', 'Jacquet', 'Axel', ''], ['labeaumb', 'Labeaume', 'Baptiste', ''], ['lambecon', 'Lambersens', 'Constant', ''], ['londechm', 'Londechal', 'Maxime', ''], ['meynetfe', 'Meynet', 'Felix', ''], ['nsakalaa', 'Nsakala', 'Adam', ''], ['pronniel', 'Pronnier', 'Lonni', ''], ['', 'fcwc', 'cwwc', 4]]], ['etudiants-m2-sts-rt-tri', [['ringa', 'Ring', 'Alexis', ''], ['assast', 'Assas', 'Tom', ''], ['combot', 'Combo', 'Tantely', ''], ['dargyd', 'D-Argy', 'Dylan', ''], ['hugong', 'Hugon', 'Gaspard', ''], ['kadjok', 'Kadjo', 'Kpangni-Koua', ''], ['koffif', 'Koffi', 'Franck', ''], ['ozbagy', 'Ozbag', 'Yunus', ''], ['bonnetd', 'Bonnet', 'Dorian', ''], ['chabaln', 'Chabal', 'Nicolas', ''], ['apouthea', 'Apouthe', 'Akpi-Joseph', ''], ['baptistg', 'Baptista-Gaspar', 'Geoffrey', ''], ['barbejul', 'Barbe', 'Julien', ''], ['bocquevi', 'Bocquet', 'Victor', ''], ['brissont', 'Brissonnet', 'Thomas', ''], ['combarea', 'Combaret', 'Adrien', ''], ['doumbifa', 'Doumbia', 'Fanta', ''], ['germaisa', 'Germain', 'Sam', ''], ['guillett', 'Guillet', 'Thomas', ''], ['hailassa', 'Hailass', 'Abdeladim', ''], ['kuitsoua', 'Kuitsouc-Danwa', 'Athena', ''], ['marti164', 'Martin', 'Alexis', ''], ['mermetma', 'Mermet', 'Matthieu', ''], ['vaussenn', 'Vaussenat', 'Nicolas', ''], ['', 'Aime', 'Adrian', 2], ['', 'Al-Sawah', 'Ahmed', 1], ['', 'fcwc', 'cwwc', 4]]]])
    return render_template('adduser.html', data=[['etudiants-l3-sts-sc-et-techno-tri', [['badair', 'Badai', 'Ryan', ''], ['cauetb', 'Cauet', 'Baptiste', ''], ['duvalc', 'Petit', 'Cyprien', ''], ['goumaa', 'Gouma', 'Archange', ''], ['ladetj', 'Ladet', 'Julien', '']]]])


@app.route('/ajout_utilisateurs_bdd', methods=['GET','POST'])
def ajout_utilisateurs_bdd():
    if request.method == 'POST':

        result = request.form
        arrEtudiants = []
        arrGroupes = []
        arrSuppression = []
        
        print(result)
        for liste in result:
            print(liste)
            etudiants = json.loads(liste)
            for etudiant in etudiants:
                userBDD = Utilisateurs.query.filter_by(uid=etudiant[0]).first()
                print(userBDD)
                if userBDD:
                    print(userBDD)
                    userBDD.classe = etudiant[4]
                    userBDD.groupe = etudiant[3]
                else:
                    user=Utilisateurs(uid=etudiant[0],nom=etudiant[1],prenom=etudiant[2],classe=etudiant[4],groupe=etudiant[3])
                    db.session.add(user)
                    serveur=serveur_un_utilisateur(liste_server())
                    attribution=attribution_vms(serveur,etudiant[0])
                arrEtudiants.append(etudiant[0])
                arrGroupes.append(etudiant[4])

                db.session.commit()

    for grp in arrGroupes:
        r = Utilisateurs.query.with_entities(Utilisateurs.uid).filter_by(classe=grp).all()
        for etu in r:
            if etu[0] not in arrEtudiants:
                arrSuppression.append(etu)
    print("suppression")
    print(arrSuppression)

    #TODO
    #La pop-up jolie

    for etu in arrSuppression:
        print(etu)
        userBDDDelete = Utilisateurs.query.filter_by(uid=etu[0]).first()
        for vm in userBDDDelete.machines_Virtuelles:
            db.session.delete(vm)
            db.session.commit()
        userBDDDelete.serveurs.clear()
        db.session.delete(userBDDDelete)
        db.session.commit()
            

    users=Utilisateurs.query.all()
    return render_template('index.html',users=users)

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
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
               {{ form.csrf_token }}
                <div class="form-group">{{ form.username.label }}: {{ form.username() }}</div>
                <div class="form-group">{{ form.password.label }}: {{ form.password() }}</div>
                <input type='submit' name='login'/>
               </form>
               '''
    elif request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            c = Conf('config/app.conf')
            username = request.form['username']
            password = request.form['password']

            if username=='root':
                mdp_Root = c.readOption("AUTHENTIFICATION","mot_de_passe_root")
                passwd, salt = mdp_Root.split(':')
                if passwd == hashlib.sha256(salt.encode() + password.encode()).hexdigest():
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
    if request.method == 'POST':
        result = request.form
        # listenomserver=[]
        # listeserver=Serveurs.query.all()
        # for serv in listeserver:
        #     listenomserver.append((serv.nom,len(serv.machines_Virtuelles)))
        # print(listenomserver)
        # rep_serv=LoadBalancing(listenomserver)
        # serveur=rep_serv.
        serveur=serveur_un_utilisateur(liste_server())
        
        # serveur="mau-59-serv14"
        attribution=attribution_vms(serveur,result['uid'])
        # machine = Machines_Virtuelles(nom=attribution[0],adresse_IP=attribution[1],adresse_MAC=attribution[3],port_RDP=attribution[4],commentaire='Vm de '+attribution[5])

        return redirect(url_for('admin_user'))

def liste_server():
    liste={}
    serveur = Serveurs.query.all()
    for serv in serveur:
        liste[serv.nom]=len(serv.machines_Virtuelles)
    return liste

#Fonction de lancement de script pour l'attribution des vms
def attribution_vms(serveur,uid):
    c = Conf('config/app.conf')
    liste_rdp=[]
    ip_used=[]
    mac_used=[]

    user=Utilisateurs.query.filter_by(uid=uid).first()
    nom_user=user.prenom
    if len(user.machines_Virtuelles)==0:
        nom=uid+'-0'
    else:
        nb=0
        tab_num=[]
        for vm in user.machines_Virtuelles:
            num=vm.nom.split("-")
            tab_num.append(int(num[1]))
        nom=uid+'-'+str(max(tab_num)+1)

    vm_RDP=Serveurs.query.filter_by(nom=serveur).first()
    for vm in range(0,len(vm_RDP.machines_Virtuelles)):
        liste_rdp.append(vm_RDP.machines_Virtuelles[vm].port_RDP)

    vms=Machines_Virtuelles.query.all()
    for vm in vms:
        ip_used.append(vm.adresse_IP)
        mac_used.append(vm.adresse_MAC)

    vma=attribution_vm(c.readOption("IP","plage_ip_debut"),c.readOption("IP","plage_ip_fin"),ip_used,liste_rdp,c.readOption("RDP","port_rdp_debut"),c.readOption("RDP","port_rdp_fin"),c.readOption("MAC","plage_mac_debut"),c.readOption("MAC","plage_mac_fin"),mac_used)
    
    comm = 'Vm de '+nom_user
    machine = Machines_Virtuelles(nom=nom,adresse_IP=vma[0],adresse_MAC=vma[1],port_RDP=vma[2],commentaire=comm)

    #TODO
    #il faut donner les identifiants de l'admin

    #reservation_base_machine(vma[0], vma[1], nom, comm, user, password)

    serveur = Serveurs.query.filter_by(nom=serveur).first()
    utilisateur = Utilisateurs.query.filter_by(uid=uid).first()

    utilisateur.serveurs.append(serveur)
    utilisateur.machines_Virtuelles.append(machine)
    serveur.machines_Virtuelles.append(machine)

    db.session.add_all([utilisateur,serveur,machine])
    db.session.commit()

#Fonction de retour pour supprimer une vm    
@app.route('/supprimer_vm', methods=['POST'])
@login_required
def del_vms():
    if request.method == 'POST':
        result = request.form
        vm=Machines_Virtuelles.query.filter_by(nom=result['nom']).first()
        db.session.delete(vm)
        db.session.commit()
        return redirect(url_for('admin_vms'))

def reservation_base_machine(ip, mac, nom, commentaire, user, password):
# TODO À Déplacer dans config
    adresse = "https://dsi.univ-savoie.fr/bm/addMachine.php"
    data = {'IPAddress':ip, 'MacAddress':mac, 'MName':nom, 'Comment':commentaire}
    r = requests.post(url = adresse, data = data, auth = (user, password))

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
        return redirect(url_for('admin_user'))

#Fonction de retour pour supprimer un utilisateur
@app.route('/supprimer_utilisateur', methods=['POST'])
@login_required
def del_user():
    if request.method == 'POST':
        result = request.form
        user=Utilisateurs.query.filter_by(uid=result['uid']).first()
        
        for vm in user.machines_Virtuelles:
            db.session.delete(vm)
            db.session.commit()
        user.serveurs.clear()
        db.session.delete(user)
        db.session.commit()
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
        for vm in serv.machines_Virtuelles:
            db.session.delete(vm)
        db.session.delete(serv)
        db.session.commit()
    return redirect(url_for('config'))

if __name__ == '__main__':
    app.run(debug=True)

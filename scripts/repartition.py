# -*- coding: utf-8 -*-
import random

class Repartion_Utilisateur:
    __listeserv = []            #liste de tout les serveurs données en paramètre
    __listeetu = []             #liste de qui regroupe tout les noms des élèves
    __nbserv = 0                #nombre de serveur
    __nbpromo =0                #nombre de promo
    __listefinal = {}           #dictionnaire (clées valeur) final rendu a la fin du programme
    __listeaffectation = []     #liste avec user répartie qui est incorporé ensuite dans la liste final

#Initialisation du programme. Construction de la listeetu, de la listeserv, du compteur de promo et du nb de srv
    def __init__(self, liste, server):
        for listepromo in liste:
            self.__nbpromo += 1
            for listegroupe in listepromo[1]:
                self.__listeetu.append(listegroupe)
        self.__listeserv = server
        self.__nbserv = len(self.__listeserv)

    def __init__(self, server):
        self.__listeserv = server
        self.__nbserv = len(self.__listeserv)

#Fonction qui fait la répartition des utilisateurs par rapport au srv.
    def userBalancing(self):
        #print("Liste d'etu:" + str(self.__listeetu))
        #print("Liste de serv " + str(self.__listeserv))
        for i in range(self.__nbserv):
            tabsrv = []
            self.__listeaffectation.append(tabsrv)
        for utilisateur in self.__listeetu:
            servchoisi = random.randint(0, self.__nbserv - 1)
            #print("serveur choisi " + str(servchoisi))
            self.__listeaffectation[servchoisi].append(utilisateur)
        #print("Liste d'affectation " + str(self.__listeaffectation))
        for i in range(len(self.__listeserv)):
            self.__listefinal[self.__listeserv[i]] = self.__listeaffectation[i]
        #print("Liste final rendu " + str(self.__listefinal))
        return self.__listefinal

#Fonction utilisé lors de l'ajout de 1 utilisateur. utilise servlessuse
    def attr_server_user(self):
        lessuse = self.servLessUse()
        #print("le moins utilisé " + str(lessuse))
        #print("Nom le moins utilisé " + str(self.__listeserv[lessuse]))
        return self.__listeserv[lessuse]

#Fonction qui retourne le serveur le moins chargé
    def servLessUse(self):
        taille = []
        for nserv in self.__listeaffectation:
            taille.append(len(nserv))
        return taille.index(min(taille))  

def serveur_plusieur_utilisateur(dicto_serveur,liste_utilisateur):
    dico_utilisateur={}
    for serveur in dicto_serveur:
        dico_utilisateur[serveur]=list()

    for utilisateur in liste_utilisateur:
        serv=choix_serveur(dicto_serveur)
        dicto_serveur[serv]=dicto_serveur[serv]+1
        dico_utilisateur[serv].append(utilisateur)
    return dico_utilisateur

def serveur_un_utilisateur(dicto_serveur):
    return choix_serveur(dicto_serveur)

def choix_serveur(dicto_serveur):
    values=list(dicto_serveur.values())
    keys = list(dicto_serveur.keys())
    mini=min(values)
    if values.count(mini)>1:
        r=random.randint(0, values.count(mini)-1)
        l=[]
        for v in range(0,len(values)):
            if values[v]==mini:
                l.append(keys[v])
            v+=1
        # print(dicto_serveur)``
        return l[r]
    else:
        i=values.index(mini)
        # print(dicto_serveur)
        return keys[i]
        


# listetudiant = ["adrian","maxime","listetrim1","oui","x","y"]
# dictserver = {"serveur1":6,"serveur2":5,"serveur3":6}
# print(serveur_plusieur_utilisateur(dictserver,listetudiant))
# print(choix_serveur(dictserver))

# unetudiant = ("trim1",["constant"])
# l=Repartion_Utilisateur(listetudiant, listeserver)
# l.userBalancing()
# l.attr_server_user()

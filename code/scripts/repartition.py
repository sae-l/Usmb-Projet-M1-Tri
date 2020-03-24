# -*- coding: utf-8 -*-
import random

# Fonction utiliser pour automatiser la fonction, elle prend une liste d'utilisateur en plus du dico des serveurs
# 
def serveur_plusieur_utilisateur(dicto_serveur,liste_utilisateur):
    # ont creer un dico dont les clef sont les serveur
    dico_utilisateur={}
    for serveur in dicto_serveur:
        dico_utilisateur[serveur]=list()

    # Pour tout les uilisateurs ont demande un serveur, et ont ajoute ceux-ci au dictionnaire de serveur en tant que valeur
    for utilisateur in liste_utilisateur:
        serv=choix_serveur(dicto_serveur)
        dicto_serveur[serv]=dicto_serveur[serv]+1
        dico_utilisateur[serv].append(utilisateur)
    return dico_utilisateur

# Fonction utiliser pour recuperer que un serveur dans le cas de l'ajout d'une seule vm
def serveur_un_utilisateur(dicto_serveur):
    return choix_serveur(dicto_serveur)

# Fonction qui donne le serveur à attribué, donne le serveur le moins peuplé sinon si il en a plusieur fait un rand
def choix_serveur(dicto_serveur):
    values=list(dicto_serveur.values())
    keys = list(dicto_serveur.keys())
    mini=min(values)
    # si il a plusieurs serveur avec le minimum de vm dessus
    if values.count(mini)>1:
        # Ont prend un nombre random entre 0 et le nombre de machine au min -1
        r=random.randint(0, values.count(mini)-1)
        l=[]
        # On fait la liste de ses machines
        for v in range(0,len(values)):
            if values[v]==mini:
                l.append(keys[v])
            v+=1
            # On retourne la machine prise dans la liste par rapport au nombre aleatoire
        return l[r]
    # Si il n'y a qu'un seul serveur à avoir moins de vm que les autre ont le retourne
    else:
        i=values.index(mini)
        return keys[i]
        


# listetudiant = ["adrian","maxime","listetrim1","oui","x","y"]
# dictserver = {"serveur1":6,"serveur2":5,"serveur3":6}
# print(serveur_plusieur_utilisateur(dictserver,listetudiant))
# print(choix_serveur(dictserver))

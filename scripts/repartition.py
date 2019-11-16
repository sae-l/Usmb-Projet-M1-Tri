# -*- coding: utf-8 -*-
import random

class LoadBalancing:
    __listeserv = []
    __listeetu = []
    __nbserv = 0
    __nbpromo =0
    __listefinal = {}
    __listeaffectation = []

    def __init__(self, liste, server):
        for listepromo in liste:
            self.__nbpromo += 1
            for listegroupe in listepromo[1]:
                self.__listeetu.append(listegroupe)
        self.__listeserv = server
        #for listeserver in self.__listeserv:
        #    self.__listefinal = {listeserver : None}
        self.__nbserv = len(self.__listeserv)


    def loadBalancing(self):
        print(self.__listeetu)
        print(self.__listeserv)
        for i in range(self.__nbserv):
            tabsrv = []
            self.__listeaffectation.append(tabsrv)
        for utilisateur in self.__listeetu:
            servchoisi = random.randint(0, self.__nbserv - 1)
            print("serveur choisi " + str(servchoisi))
            self.__listeaffectation[servchoisi].append(utilisateur)
        print(self.__listeaffectation)
        for i in range(len(self.__listeserv)):
            self.__listefinal[self.__listeserv[i]] = self.__listeaffectation[i]
        print(self.__listefinal)

#refaire avec prise en compte de la liste serv + etu donné en paramètre
    def adduser(self,unetudiant):
        #nom = unetudiant[1]
        lessuse = self.servLessUse()
        print("le moins utilisé " + str(lessuse))
        #self.__listefinal[self.__listeserv[lessuse]] = nom[0]
        print(self.__listeserv[lessuse])
        return self.__listeserv[lessuse]

    def servLessUse(self):
        taille = []
        for nserv in self.__listefinal:
            taille.append(len(nserv))
        return taille.index(min(taille))



listetudiant = [("listetrim2",["adrian","maxime"]),("listetrim1",["oui"])]
listeserver = ["serveur1","serveur2","serveur3"]
unetudiant = ("trim1",["constant"])
l=LoadBalancing(listetudiant, listeserver)
l.loadBalancing()
l.adduser(unetudiant)

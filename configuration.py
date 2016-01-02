#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  configuration.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#

def ecrireDefauts():
    #   Permet d'enregistrer les paramètres par défaut dans un fichier de configuration
    #
    
    defauts = {"minVBat":32.4,        #Batterie à 0% : 10.8*3
               "maxVBat":40.8,        #Batterie à 100% : 13.6*3
               "capBat":12,           #Capacité en Ah
               "Pmax":1500,           #Puissance electrique maximale du moteur
               "Imax":50.,            #Adapter en fonction du capteur (valeur de Imax en A pour 1023 renvoyé par le capteur)
               "I0":512,              #Valeur envoyée par le capteur pour I = 0A
               "Vmax":100,            #Vitesse maximale en km/h
               "majMoy":3,            #Taux d'actualisation des moyennes (1 pour 30fps, 30 pour 1fps)
               "tempo":0.5}           #Taux d'actualisation des logs (en secondes)
    
    ecrireConf(defauts)

def ecrireConf(parametres):
    #   Permet d'enregistrer les paramètres dans un fichier de configuration
    # 
    #   @param : 
    #       parametres : dictionnaire contenant les données à écrire
    #
    
    fichier = open("conf/HyBike.conf","w")
    for key in parametres:
        fichier.write(str(key) + ":" + str(parametres[key]) + ":" + str(type(parametres[key])) + "\n")
    
    fichier.close()
    
def lireConf():
    #   Permet de lire les paramètres stockés dans un fichier de configuration
    # 
    #   @return : 
    #       parametres : dictionnaire contenant les données lues
    #
    
    parametres = {}
    
    try:
        fichier = open("conf/HyBike.conf","r")
    except FileNotFoundError:
        ecrireDefauts()
        fichier = open("conf/HyBike.conf","r")
    
    for line in fichier:
        ligne = line[:len(line)-1]
        ligne = ligne.split(":")
        if ligne[2] == "<class 'float'>":
            parametres[ligne[0]] = float(ligne[1])
        else:
            parametres[ligne[0]] = int(ligne[1])
    
    fichier.close()
    return parametres

if __name__ == '__main__':
    
    import os
    
    print(lireConf())
    os.system("rm conf/HyBike.conf")

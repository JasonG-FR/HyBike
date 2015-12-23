#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  logSession.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#

def logSession(fichier,datas,compteur,tempo=1):
    #   Permet d'enregistrer les données reçue par Arduino dans un fichier csv
    # 
    #   @param : 
    #       fichier : le fichier dans lequel écrire les données
    #       data : série de données à enregistrer (liste de strings au format [tps,acc,frein,ubat,imot,vit])
    #       compteur : variable permettant de connaitre la position du cycle par rapport à la tempo (-1 pour init)
    #       tempo : temporisation pour enregistrer les données (en seconde)
    #
    
    txTrans = 1/30.     #temps de cycle d'envoi des données par Arduino en secondes
    
    #Si on est au début du fichier (caractère 0)
    if compteur[0] >= int(tempo/txTrans) or compteur[0] == -1:

        if fichier.tell() == 0:
            #On écrit l'entête
            fichier.write("Temps (s);Accélération (%);Freinage (%);Tension batterie (V);Intensité moteur (A);Vitesse (km/h)\n")

        #On écrit les valeurs
        ligne = ""
        for data in datas:
            ligne += data + ";"
        
        fichier.write(ligne[:len(ligne) - 1] + "\n")    #On enlève le dernier ";"
        
        datas[0] = str(int(datas[0]) + tempo)
        compteur[0] = 0
    
    compteur[0] += 1

if __name__ == '__main__':
    
    from time import sleep
    import os
    
    f = open("test.csv","w")
    donnees =  ["0","50","50","12","5","45"]
    cpt = [-1]
    
    for i in range(25*30):
        logSession(f,donnees,cpt)
    
    f.close()
    
    f = open("test.csv","r")
    print("Affichage du fichier généré :\n")
    for line in f:
        print(line[:len(line)-1])
    f.close()
    os.system("rm test.csv")

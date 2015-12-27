#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  logSession.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#

import time

def logSession(fichier,datas,tempsConsigne,tempo=1):
    #   Permet d'enregistrer les données reçue par Arduino dans un fichier csv
    # 
    #   @param : 
    #       fichier : le fichier dans lequel écrire les données
    #       data : série de données à enregistrer (liste de strings au format [tps,acc,frein,ubat,imot,vit])
    #       tempsConsigne : variable stockant la valeur du temps limite de la tempo (liste d'une valeur pour qu'elle soit modifiable)
    #       tempo : temporisation pour enregistrer les données (en seconde)
    #
    
    
    #Si la tempo est atteinte
    #print(str(time.time()) + ">=" + str(tempsConsigne[0]) + " : " + str(time.time() >= tempsConsigne[0]))
    if time.time() >= tempsConsigne[0]:
        
        #On met à jour la consigne de temps
        tempsConsigne[0] = time.time() + tempo
        
        #Si on est au début du fichier (caractère 0)
        if fichier.tell() == 0:
            #On écrit l'entête
            fichier.write("Temps (s);Accélération (%);Freinage (%);Tension batterie (V);Intensité moteur (A);Vitesse (km/h)\n")

        #On écrit les valeurs
        ligne = ""
        for data in datas:
            ligne += data + ";"
        
        fichier.write(ligne[:len(ligne) - 1] + "\n")    #On enlève le dernier ";"
        
        if tempo%1 != 0:
            #Tempo non entière
            datas[0] = "{0:.2f}".format(float(datas[0]) + tempo)
        else:
            datas[0] = str(int(datas[0]) + tempo)

if __name__ == '__main__':
    
    from time import sleep
    import os
    
    f = open("test.csv","w")
    donnees =  ["0","50","50","12","5","45"]
    tps = [0]
    
    for i in range(25*30):
        logSession(f,donnees,tps,1)
        sleep(1/30.)
    
    f.close()
    
    f = open("test.csv","r")
    print("Affichage du fichier généré :\n")
    for line in f:
        print(line[:len(line)-1])
    f.close()
    os.system("rm test.csv")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  getData.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#

from tkinter import *
import serial

from fonctionsArduino import *
from updateData import *


def getData(ser, fenetre, tkVars, tkObj, moyennes, params):
    #   Permet de lancer l'acquisition continue des données depuis Arduino
    # 
    #   @param : 
    #       ser : objet contenant la connection au port série (connection avec Arduino)
    #       fenetre : objet contenant la fênetre à actualiser
    #       tkVars : dictionnaire contenant toutes les variables de l'affichage
    #       tkObj : dictionnaire contenant tous les objets à modifier
    #       moyennes : dictionnaire qui contient toutes les séries de données utilisées pour le calcul des moyennes
    #       params : dictionnaire contenant les valeurs des paramètres
    #
    #    
    
    data = {}
    tpsConsigne = [0]
    fichier = 0
    
    #Flush du tampon d'Arduino
    ser.flushInput()
    
    while(True):
        #Lecture des données issues d'Arduino
        dataTab = decodageArduino(ser)
        
        #Mise à jour des variables et de l'affichage
        if tkVars["logON"].get():
            #On crée le fichier s'il n'existe pas
            if fichier == 0:
                
                fichier = open(nomLog(),"w")
                #[tps,acc,frein,ubat,imot,vit]
                donnees = ["0","0","0","0","0","0"]
        
            updateData(tkVars, tkObj, moyennes, params, dataTab, data, fichier, tpsConsigne, params["tempo"], donnees)
        else:
            #On ferme le fichier s'il est ouvert
            if fichier != 0:
                fichier.close()
                fichier = 0
            
            updateData(tkVars, tkObj, moyennes, params, dataTab, data)
    
        try:
            fenetre.update()
        except TclError:
            break

if __name__ == '__main__':
    exit()

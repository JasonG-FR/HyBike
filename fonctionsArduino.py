#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  fonctionsArduino.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  


def decodageArduino(ser):
    #   Permet de décoder les valeurs envoyées par l'arduino
    # 
    #   @param : 
    #       ser : objet contenant la liaison série avec l'arduino
    #
    #   @return :
    #       une liste contenant toutes les valeurs de l'arduino
    # 
    #
    
    #Format de donnée csv avec ";" comme séparateur : le format recu est : b'0000;2222;2222\n'
    dataRaw = ser.readline()
        
    #On décode la variable octale et on supprime les caractères spéciaux (\n)
    dataRaw = dataRaw.decode("utf-8")
    dataRaw = dataRaw.replace("\n","")
        
    """Séparation des variables"""
    return dataRaw.split(";")

def convArduino(dataTab, data):
    #   Permet de convertir les valeurs binaires en valeurs utilisables et les enregistrer dans un dictionnaire
    # 
    #   @param : 
    #       dataTab : liste contenant les valeurs de l'arduino (issue de decodageArduino)
    #       data : dictionnaire contenant les valeurs convertie et classées
    # 
    #
    
    #Format Arduino : acc;frein;batt;intensité;vitesse
    data["valAcc"] = int(int(dataTab[0])/1023*100)
    data["valFrein"] = int(int(dataTab[1])/1023*100)
    data["valBatt"] = int(int(dataTab[2])/1023*100)
    data["valIntensite"] = int(dataTab[3])
    data["valVitesse"] = int(dataTab[4])/1023.*100

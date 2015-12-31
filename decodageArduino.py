#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  decodageArduino.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#  


def decodageArduino(ser):
    #Format de donnée csv avec ";" comme séparateur : le format recu est : b'0000;2222;2222\n'
    dataRaw = str(ser.readline())
        
    #On enlève le premier caractère (b pour signaler une variable octale) et les caractères spéciaux (' et \n)
    dataRaw = dataRaw[1:]
    dataRaw = dataRaw.replace("'","")
    dataRaw = dataRaw.replace("\\n","")
        
    """Séparation des variables"""
    return dataRaw.split(";")

def convArduino(dataTab, data):
    #Format Arduino : acc;frein;batt;intensité;vitesse
    data["valAcc"] = int(int(dataTab[0])/1023*100)
    data["valFrein"] = int(int(dataTab[1])/1023*100)
    data["valBatt"] = int(int(dataTab[2])/1023*100)
    data["valIntensite"] = int(dataTab[3])
    data["valVitesse"] = int(dataTab[4])/1023.*100

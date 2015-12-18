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

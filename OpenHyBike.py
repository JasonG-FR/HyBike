#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  OpenHyBike.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#   License :
#  
#  

import serial

from HyBike import *
from interfaceParametres import *

def main():
    
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        ser.readline()
    except serial.serialutil.SerialException:
        print("Arduino non connecté!")
        exit()
        
    changeParam = [False]
    
    #On lance l'interface principale
    HyBike(changeParam,ser)
    
    #Tant qu'on veux changer les paramètres
    while changeParam[0]:
        #On lance l'interface des paramètres
        interfaceParametres()
        changeParam[0] = False
        #Puis on relance l'interface principale
        HyBike(changeParam,ser)

if __name__ == '__main__':
    
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  OpenHyBike.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
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

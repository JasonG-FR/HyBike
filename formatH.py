#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  formatH.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  


def formatH(heures):
    #   Permet de formater un temps en heure flottante (1.25h) en heure classique (1:15)
    # 
    #   @param : 
    #       heures contient un temps en heures au format float
    #   @return :
    #       heure au format str : hh:mm
    # 
    #
    
    HH = int(heures)
    MM = heures - HH
    MM *= 60
    MM = int(MM)
    
    H = str(HH)
    if MM < 10:
        M = "0" + str(MM)
    else:
        M = str(MM)
    
    return H + ":" + M

if __name__ == '__main__':
    
    print("1.5h = " + formatH(1.5))
    print("1.25h = " + formatH(1.25))
    print("1.8525741h = " + formatH(1.8525741))
    print("1.05h = " + formatH(1.05))

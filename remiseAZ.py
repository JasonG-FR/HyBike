#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  remiseAZ.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#

from tkinter import *

def remiseAZ(*args):
    #   Permet de remettre les moyennes à zéro (base de donnée et affichage)
    # 
    #   @param : 
    #       La fonction peut recevoir deux types de paramètres :
    #           dictionnaires de valeurs au format {"clé1":valeur,"clé2":valeur,"clé3":valeur}
    #           variables d'affichage des valeurs
    # 
    #
    
    for arg in args:
        
        #Si c'est un dictionnaire
        if type(arg) == type({}):
            for key in arg:
                arg[key] = 0
        
        #Si c'est une variable d'affichage
        elif str(type(arg)) == "<class 'tkinter.StringVar'>":
            #Si le dernier caractère est W il s'agit de la puissance moyenne
            if arg.get()[len(arg.get())-1] == "W":
                arg.set("0 W")
            #Sinon si le dernier caractère est h alors il s'agit de la vitesse moyenne
            elif arg.get()[len(arg.get())-1] == "h":
                arg.set("Vitesse moyenne : 0.0 km/h")


if __name__ == '__main__':
    
    fenetre = Tk()
    
    test = {"Vitesse":5485,"Temps":547,"Tension":45,"Intensité":88}
    test2 = {"Vitesse":225,"Température":147,"Tension":8745,"Intensité":758}
    test3 = StringVar()
    test3.set("548 W")
    test4 = StringVar()
    test4.set("25 km/h")
    
    print(test)
    print(test2)
    print(test3.get())
    print(test4.get())
    remiseAZ(test,test2,test3,test4)
    print(test)
    print(test2)
    print(test3.get())
    print(test4.get())

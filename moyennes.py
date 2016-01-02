#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  moyennes.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
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
            #Si l'argument n'est pas vide
            if arg.get() != "":
                #Si le dernier caractère est W il s'agit de la puissance moyenne
                if arg.get()[len(arg.get())-1] == "W":
                    arg.set("0 W")
                #Sinon si le dernier caractère est h alors il s'agit de la vitesse moyenne
                elif arg.get()[len(arg.get())-1] == "h":
                    arg.set("Vitesse moyenne : 0.0 km/h")


def moyenneDynamique(serie,valeur,drop=1):
    #   Permet d'afficher la moyenne en temps réel sans stocker toutes les valeurs intérmédiaires
    #   (plus rapide et moins d'utilisation mémoire)
    # 
    #   @param : 
    #       serie contient un dictionnaire au format {"moy":valeur,"nb":valeur,"i":valeur}
    #       valeur contient la valeur à ajouter à la moyenne
    #       drop permet d'indiquer combien de mesures doivent être ignorées (2 indique 1 mesure sur 2)
    # 
    #
    
    if serie["i"] <= 1:
        serie["moy"] *= serie["nb"]
        serie["moy"] += valeur
        serie["nb"] += 1
        serie["moy"] /= serie["nb"]
        serie["i"] = drop
    else:
        serie["i"] -= 1
    

if __name__ == '__main__':
    from random import *
    
    liste = []
    for i in range(100000):
        liste.append(randrange(0, 101, 2))  # Entier entre 0 et 100
        
    print("Calcul de la moyenne :")
    moy1 = 0
    for item in liste:
        moy1 += item
    moy1 = moy1/float(len(liste))
    print(moy1)
    
    print("Test de la fonction moyenneDynamique :")
    serie = {"moy":0,"nb":0,"i":0}
    for item in liste:
        moyenneDynamique(serie,item)
    print(serie["moy"])
    
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

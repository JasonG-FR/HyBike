#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  moyenneDynamique.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#


def moyenneDynamique(serie,valeur):
    #   Permet d'afficher la moyenne en temps réel sans stocker toutes les valeurs intérmédiaires
    #   (plus rapide et moins d'utilisation mémoire)
    # 
    #   @param : 
    #       serie contient un dictionnaire au format {"moy":valeur,"nb":valeur}
    #       valeur contient la valeur à ajouter à la moyenne
    # 
    #
    
    serie["moy"] *= serie["nb"]
    serie["moy"] += valeur
    serie["nb"] += 1
    serie["moy"] /= serie["nb"]
    

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
    serie = {"moy":0,"nb":0}
    for item in liste:
        moyenneDynamique(serie,item)
    print(serie["moy"])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  moyenneDynamique.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#


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

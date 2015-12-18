#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  moyenneDynamique.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#


def main(serie,valeur):
    #   Permet d'afficher la moyenne en temps réel sans stocker toutes les valeurs intérmédiaires
    #   (plus rapide et moins d'utilisation mémoire)
    # 
    #   @param : 
    #       serie contient un dictionnaire au format {"moyenne":valeur,"nombre":valeur}
    #       valeur contient la valeur à ajouter à la moyenne
    # 
    #
    
    serie["moyenne"] *= serie["nombre"]
    serie["moyenne"] += valeur
    serie["nombre"] += 1
    serie["moyenne"] /= serie["nombre"]
    

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
    serie = {"moyenne":0,"nombre":0}
    for item in liste:
        main(serie,item)
    print(serie["moyenne"])

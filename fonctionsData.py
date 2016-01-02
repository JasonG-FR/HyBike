#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  fonctionsData.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  
#  

from tkinter import *


def convBinNumCentre(zeroBin,valeurBin,maxVal):
    #   Permet de réaliser la conversion binaire - numérique lorsque le zéro numérique n'est pas le zéro binaire
    #   ex :    bin :   0   255     512     <-->       0     zeroBin  2zeroBin
    #           num : -15    0       15     <-->    -maxVal     0     maxVal
    # 
    #   @param : 
    #       zeroBin : valeur binaire pour une valeur numérique nulle (int)
    #       valeurBin : valeur binaire à convertir (int)
    #       maxVal : valeur numérique lorsque valeurBin = 2 x zeroBin
    #
    #
    
    tauxEch = maxVal/zeroBin
    return (valeurBin-zeroBin)*tauxEch

def majProgressBar(data,val,valStr,precision=-1,unite="%"):
    #   Permet de mettre à jour les valeurs des barres d'avancement (Progress Bar)
    # 
    #   @param : 
    #       data : valeur issue de l'arduino (int)
    #       val : Int ou Float Tk pour la variable de progress bar
    #       valStr : Str Tk pour affichage textuel de la valeur
    #       precision : int indiquant le nombre de decimales à afficher si la valeur est un float
    #       unite : texte à afficher après la valeur
    #
    #
    
    val.set(data)
    
    if str(type(data)) == "<class 'int'>":
        valStr.set(str(data) + " " + unite)
    else:
        valStr.set(("{0:." + str(precision) + "f}").format(data) + " " + unite)
    
def majCouleur(data,label,cHaut,moy,cMoy,bas=-1,cBas="black"):
    #   Permet de mettre à jour la couleur des variables
    # 
    #   @param : 
    #       data : valeur issue de l'arduino (int)
    #       label : l'objet texte Tk à changer de couleur
    #       cHaut : couleur si au-dessus du seuil moyen
    #       moy : seuil moyen
    #       cMoy : couleur si en-dessous du seuil moyen
    #       bas : seuil bas
    #       cBas : couleur si en-dessous du seuil bas
    #
    #
    
    def colorer(objet,couleur):
        try:
            objet.configure(foreground=couleur)
        except TclError:
            return 1
    
    #On vérifie si on a un ou deux seuils
    if bas == -1:
        if data > moy:
            colorer(label,cHaut)
        else:
            colorer(label,cMoy)
        
    else:
        if data > moy:
            colorer(label,cHaut)
        elif data > bas:
            colorer(label,cMoy)
        else:
            colorer(label,cBas)

if __name__ == '__main__':
    exit()

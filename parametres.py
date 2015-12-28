#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  parametres.py
#  
#

from tkinter import *
from configuration import *

def saveParam(variables):
    #   Permet d'enregistrer les paramètres dans le fichier de configuration
    #
    #   @param
    #       variables : contient une liste de toutes les variables de l'interface
    #
    
    params = {}
    keys = ["minVBat","maxVBat","capBat","Pmax","Imax","I0","Vmax","majMoy","tempo"]
    for i in range(len(variables)):
        #Si la variable représente un float (min et max VBat, Imax)
        if i in [0,1,4]:
            params[keys[i]] = float(variables[i].get())
        #Si majMoy
        elif i == 7:
            params[keys[i]] = 30./float(variables[i].get())
        #Si tempo
        elif i == 8:
            params[keys[i]] = 1./float(variables[i].get())
        #Sinon c'est des int
        else:
            params[keys[i]] = int(variables[i].get())
    
    ecrireConf(params)

def lireParam(variables):
    #   Permet de lire les paramètres du fichier de configuration et de les associer aux variables
    #
    #   @param
    #       variables : contient une liste de toutes les variables de l'interface
    #
    
    keys = ["minVBat","maxVBat","capBat","Pmax","Imax","I0","Vmax","majMoy","tempo"]
    params = lireConf()
    for i in range(len(variables)):
        #S'il s'agit de la fréquence de maj des moyennes
        if i == 7:
            variables[i].set(str(1/(params[keys[i]]/30.)))      #!! présenté comme frequence (nb fois/sec) à convertir!!
        #S'il s'agit de la fréquence de maj des logs
        elif i == 8:
            variables[i].set(str(1./params[keys[i]]))             #!! présenté comme frequence (nb fois/sec) à convertir!!
        else:
            variables[i].set(str(params[keys[i]]))

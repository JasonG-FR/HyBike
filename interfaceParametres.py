#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  interfaceParametres.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#  
#

from tkinter import *
from tkinter import ttk
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
    
    

def interfaceParametres():
    #   Permet d'afficher, de modifier et d'enregistrer les paramètres du fichier de configuration
    #
    #   @return :
    #       params : dictionnaire contenant toutes les valeurs à jour
    #

    def majParam(*args):
        saveParam(paramVars)
        fenetre.destroy()
    
    def razParam(*args):
        ecrireDefauts()
        lireParam(paramVars)
    
    """Interface"""
    fenetre = Tk()
    fenetre.title("Paramètres")
    fenetre.geometry("800x480")
    
    """Variables"""
    minVBat = StringVar()
    maxVBat = StringVar()
    capBat = StringVar()
    Pmax = StringVar()
    Imax = StringVar()
    I0 = StringVar()
    Vmax = StringVar()
    majMoy = StringVar()    #!! présenté comme frequence (nb fois/sec) à convertir!!
    tempo = StringVar()     #!! présenté comme frequence (nb fois/sec) à convertir!! 
    paramVars = [minVBat,maxVBat,capBat,Pmax,Imax,I0,Vmax,majMoy,tempo]
    
    #Lecture des valeurs
    lireParam(paramVars)
    
    
    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=0, row=0, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)

    #Cadre Batterie
    frameBat = ttk.Labelframe(cadre, text=' Batterie ', padding="5 5 5 5")
    frameBat.grid(column=1, row=1, sticky=(N, W, E, S), padx=5, pady=5)

    ttk.Label(frameBat, text="Tension à 0% : ").grid(column=1, row=1)
    Spinbox(frameBat, width=5, from_=0.0, to=100.0, increment=0.1 ,textvariable=minVBat).grid(column=2, row=1)
    ttk.Label(frameBat, text=" V").grid(column=3, row=1)
    
    ttk.Label(frameBat, text="Tension à 100% : ").grid(column=1, row=2)
    Spinbox(frameBat, width=5, from_=0.0, to=100.0, increment=0.1 ,textvariable=maxVBat).grid(column=2, row=2)
    ttk.Label(frameBat, text=" V").grid(column=3, row=2)
    
    ttk.Label(frameBat, text="Capacité : ").grid(column=1, row=3)
    Spinbox(frameBat, width=5, from_=0, to=200, increment=1 ,textvariable=capBat).grid(column=2, row=3)
    ttk.Label(frameBat, text=" Ah").grid(column=3, row=3)
    
    #Cadre Moteur
    frameMot = ttk.Labelframe(cadre, text=' Moteur électrique ', padding="5 5 5 5")
    frameMot.grid(column=1, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameMot, text="Puissance max : ").grid(column=1, row=1)
    Spinbox(frameMot, width=5, from_=0, to=3000, increment=1 ,textvariable=Pmax).grid(column=2, row=1)
    ttk.Label(frameMot, text=" W").grid(column=3, row=1)
    
    ttk.Label(frameMot, text="Imax capteur : ").grid(column=1, row=2)
    Spinbox(frameMot, width=5, from_=0.0, to=200.0, increment=0.1 ,textvariable=Imax).grid(column=2, row=2)
    ttk.Label(frameMot, text=" A").grid(column=3, row=2)
    
    ttk.Label(frameMot, text="Valeur capteur 0A : ").grid(column=1, row=3)
    Spinbox(frameMot, width=5, from_=0, to=1023, increment=1 ,textvariable=I0).grid(column=2, row=3)
    ttk.Label(frameMot, text="  ").grid(column=3, row=3)
    
    #Cadre Dashboard
    frameDash = ttk.Labelframe(cadre, text=' Dashboard ', padding="5 5 5 5")
    frameDash.grid(column=2, row=1, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameDash, text="Vitesse max : ").grid(column=1, row=1)
    Spinbox(frameDash, width=5, from_=0, to=200, increment=1 ,textvariable=Vmax).grid(column=2, row=1)
    ttk.Label(frameDash, text=" km/h").grid(column=3, row=1)
    
    ttk.Label(frameDash, text="Freq actu moyennes : ").grid(column=1, row=2)
    Spinbox(frameDash, width=5, from_=0.1, to=30.0, increment=0.1 ,textvariable=majMoy).grid(column=2, row=2)
    ttk.Label(frameDash, text=" /s").grid(column=3, row=2)
    
    #Cadre Logs
    frameLog = ttk.Labelframe(cadre, text=' Logs ', padding="5 5 5 5")
    frameLog.grid(column=2, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameLog, text="Freq relevés : ").grid(column=1, row=1)
    Spinbox(frameLog, width=5, from_=0.1, to=30.0, increment=0.1 ,textvariable=tempo).grid(column=2, row=1)
    ttk.Label(frameLog, text=" /s").grid(column=3, row=1)
    
    #Cadre bouton
    frameBouton = ttk.Frame(cadre)
    frameBouton.grid(column=1, row=3, columnspan=2)
    ttk.Button(frameBouton, text="Valider", command=majParam).grid(column=1, row=1, pady=5)
    ttk.Button(frameBouton, text="Réinitialiser", command=razParam).grid(column=2, row=1, pady=5)
    
    
    fenetre.mainloop()
    
    return lireConf()

if __name__ == '__main__':
    
    print(interfaceParametres())

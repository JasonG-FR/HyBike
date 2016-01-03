#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  interfaceParametres.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#

from tkinter import *
from tkinter import ttk
from configuration import *
from parametres import *


def interfaceParametres():
    #   Permet d'afficher, de modifier et d'enregistrer les paramètres du fichier de configuration
    #
    #
    
    def plus(tkVar, increment, maxi, unite):
        if int(tkVar.get().split(" ")[0]) < maxi:
            if str(type(increment)) == "<class 'int'>":
                tkVar.set(str(int(tkVar.get().split(" ")[0]) + increment) + unite)
            else:
                decimales = len(str(increment).split(" ")[0].split(".")[1])
                tkVar.set(("{0:." + str(decimales) + "f}").format(float(tkVar.get().split(" ")[0]) + increment) + unite)
            
    def moins(tkVar, increment, mini, unite):
        if int(tkVar.get().split(" ")[0]) > mini:
            if str(type(increment)) == "<class 'int'>":
                tkVar.set(str(int(tkVar.get().split(" ")[0]) - increment) + unite)
            else:
                decimales = len(str(increment).split(" ")[0].split(".")[1])
                tkVar.set(("{0:." + str(decimales) + "f}").format(float(tkVar.get().split(" ")[0]) - increment) + unite)
    
    def ajouterUnite(tkVar, unite):
        #tkVarStr.set(tkVar.get() + unite)
        return tkVar.get() + unite
        
    def majParam(*args):
        saveParam(paramVars)
        fenetre.destroy()
    
    def razParam(*args):
        ecrireDefauts()
        lireParam(paramVars, unites)
    
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
    majMoy = StringVar()
    tempo = StringVar()
    paramVars = [minVBat,maxVBat,capBat,Pmax,Imax,I0,Vmax,majMoy,tempo]
    unites = [" V"," V"," Ah"," W"," A"," "," km/h"," /s"," /s"]
    
    #Lecture des valeurs
    lireParam(paramVars,unites)
    
    
    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=0, row=0, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)

    #Cadre Batterie
    frameBat = ttk.Labelframe(cadre, text=' Batterie ', padding="5 5 5 5")
    frameBat.grid(column=1, row=1, sticky=(N, W, E, S), padx=5, pady=5)

    ttk.Label(frameBat, text="Tension à 0% : ").grid(column=1, row=1)
    #Spinbox(frameBat, width=5, from_=0.0, to=100.0, increment=0.1 ,textvariable=minVBat).grid(column=2, row=1)
    ttk.Label(frameBat, textvariable=minVBat).grid(column=2, row=1, padx=5)
    ttk.Button(frameBat, text="-", command=lambda : moins(minVBat,0.1,0," V"), width=2).grid(column=4, row=1)
    ttk.Button(frameBat, text="+", command=lambda : plus(minVBat,0.1,100," V"), width=2).grid(column=5, row=1)
    
    ttk.Label(frameBat, text="Tension à 100% : ").grid(column=1, row=2)
    #Spinbox(frameBat, width=5, from_=0.0, to=100.0, increment=0.1 ,textvariable=maxVBat).grid(column=2, row=2)
    ttk.Label(frameBat, textvariable=maxVBat).grid(column=2, row=2, padx=5)
    #ttk.Label(frameBat, text=" V ").grid(column=3, row=2)
    ttk.Button(frameBat, text="-", command=lambda : moins(maxVBat,0.1,0," V"), width=2).grid(column=4, row=2, pady=5)
    ttk.Button(frameBat, text="+", command=lambda : plus(maxVBat,0.1,100," V"), width=2).grid(column=5, row=2, pady=5)
    
    ttk.Label(frameBat, text="Capacité : ").grid(column=1, row=3)
    #Spinbox(frameBat, width=5, from_=0, to=200, increment=1 ,textvariable=capBat).grid(column=2, row=3)
    ttk.Label(frameBat, textvariable=capBat).grid(column=2, row=3, padx=5)
    #ttk.Label(frameBat, text=" Ah ").grid(column=3, row=3)
    ttk.Button(frameBat, text="-", command=lambda : moins(capBat,1,0," Ah"), width=2).grid(column=4, row=3)
    ttk.Button(frameBat, text="+", command=lambda : plus(capBat,1,200," Ah"), width=2).grid(column=5, row=3)
    
    #Cadre Moteur
    frameMot = ttk.Labelframe(cadre, text=' Moteur électrique ', padding="5 5 5 5")
    frameMot.grid(column=1, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameMot, text="Puissance max : ").grid(column=1, row=1)
    #Spinbox(frameMot, width=5, from_=0, to=3000, increment=1 ,textvariable=Pmax).grid(column=2, row=1)
    ttk.Label(frameMot, textvariable=Pmax).grid(column=2, row=1, padx=5)
    #ttk.Label(frameMot, text=" W ").grid(column=3, row=1)
    ttk.Button(frameMot, text="-", command=lambda : moins(Pmax,1,0," W"), width=2).grid(column=4, row=1)
    ttk.Button(frameMot, text="+", command=lambda : plus(Pmax,1,3000," W"), width=2).grid(column=5, row=1)
    
    ttk.Label(frameMot, text="Imax capteur : ").grid(column=1, row=2)
    #Spinbox(frameMot, width=5, from_=0.0, to=200.0, increment=0.1 ,textvariable=Imax).grid(column=2, row=2)
    ttk.Label(frameMot, textvariable=Imax).grid(column=2, row=2, padx=5)
    #ttk.Label(frameMot, text=" A ").grid(column=3, row=2)
    ttk.Button(frameMot, text="-", command=lambda : moins(Imax,0.1,0," A"), width=2).grid(column=4, row=2, pady=5)
    ttk.Button(frameMot, text="+", command=lambda : plus(Imax,0.1,200," A"), width=2).grid(column=5, row=2, pady=5)
    
    ttk.Label(frameMot, text="Valeur capteur 0A : ").grid(column=1, row=3)
    #Spinbox(frameMot, width=5, from_=0, to=1023, increment=1 ,textvariable=I0).grid(column=2, row=3)
    ttk.Label(frameMot, textvariable=I0).grid(column=2, row=3, padx=5)
    #ttk.Label(frameMot, text="   ").grid(column=3, row=3)
    ttk.Button(frameMot, text="-", command=lambda : moins(I0,1,0," "), width=2).grid(column=4, row=3)
    ttk.Button(frameMot, text="+", command=lambda : plus(I0,1,1023," "), width=2).grid(column=5, row=3)
    
    #Cadre Dashboard
    frameDash = ttk.Labelframe(cadre, text=' Dashboard ', padding="5 5 5 5")
    frameDash.grid(column=2, row=1, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameDash, text="Vitesse max : ").grid(column=1, row=1)
    #Spinbox(frameDash, width=5, from_=0, to=200, increment=1 ,textvariable=Vmax).grid(column=2, row=1)
    ttk.Label(frameDash, textvariable=Vmax).grid(column=2, row=1, padx=5)
    #ttk.Label(frameDash, text=" km/h ").grid(column=3, row=1)
    ttk.Button(frameDash, text="-", command=lambda : moins(Vmax,1,0," km/h"), width=2).grid(column=4, row=1)
    ttk.Button(frameDash, text="+", command=lambda : plus(Vmax,1,200," km/h"), width=2).grid(column=5, row=1)
    
    ttk.Label(frameDash, text="Freq actu moyennes : ").grid(column=1, row=2)
    #Spinbox(frameDash, width=5, from_=0.1, to=30.0, increment=0.1 ,textvariable=majMoy).grid(column=2, row=2)
    ttk.Label(frameDash, textvariable=majMoy).grid(column=2, row=2, padx=5)
    #ttk.Label(frameDash, text=" /s ").grid(column=3, row=2)
    ttk.Button(frameDash, text="-", command=lambda : moins(majMoy,0.1,0.1," /s"), width=2).grid(column=4, row=2, pady=5)
    ttk.Button(frameDash, text="+", command=lambda : plus(majMoy,0.1,30," /s"), width=2).grid(column=5, row=2, pady=5)
    
    #Cadre Logs
    frameLog = ttk.Labelframe(cadre, text=' Logs ', padding="5 5 5 5")
    frameLog.grid(column=2, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    
    ttk.Label(frameLog, text="Freq relevés : ").grid(column=1, row=1)
    #Spinbox(frameLog, width=5, from_=0.1, to=30.0, increment=0.1 ,textvariable=tempo).grid(column=2, row=1)
    ttk.Label(frameLog, textvariable=tempo).grid(column=2, row=1, padx=5)
    #ttk.Label(frameLog, text=" /s ").grid(column=3, row=1)
    ttk.Button(frameLog, text="-", command=lambda : moins(tempo,0.1,0.1," /s"), width=2).grid(column=4, row=1)
    ttk.Button(frameLog, text="+", command=lambda : plus(tempo,0.1,30," /s"), width=2).grid(column=5, row=1)
    
    #Cadre bouton
    frameBouton = ttk.Frame(cadre)
    frameBouton.grid(column=1, row=3, columnspan=2)
    ttk.Button(frameBouton, text="Valider", command=majParam).grid(column=1, row=1, pady=5)
    ttk.Button(frameBouton, text="Réinitialiser", command=razParam).grid(column=2, row=1, pady=5)
    
    fenetre.mainloop()
    

if __name__ == '__main__':
    
    interfaceParametres()

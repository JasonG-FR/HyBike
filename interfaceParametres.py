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
    
    def genLabels(fLabel, noms):
        #   Génére les libélés des paramètres
        #
        #   @params :
        #       fLabel : le Frame Tk ou afficher les libélés
        #       noms : liste des libélés dans l'ordre
        #
        
        i = 1
        for nom in noms:
            ttk.Label(fLabel, text=nom).grid(column=1, row=i, pady=6)
            i += 1
    
    def plus(tkVar, increment, maxi, unite):
        if str(type(increment)) == "<class 'int'>":
            if int(tkVar.get().split(" ")[0]) < maxi:
                tkVar.set(str(int(tkVar.get().split(" ")[0]) + increment) + unite)
        else:
            if float(tkVar.get().split(" ")[0]) < maxi:
                decimales = len(str(increment).split(" ")[0].split(".")[1])
                tkVar.set(("{0:." + str(decimales) + "f}").format(float(tkVar.get().split(" ")[0]) + increment) + unite)
            
    def moins(tkVar, increment, mini, unite):
        if str(type(increment)) == "<class 'int'>":
            if int(tkVar.get().split(" ")[0]) > mini:
                tkVar.set(str(int(tkVar.get().split(" ")[0]) - increment) + unite)
        else:
            if float(tkVar.get().split(" ")[0]) > mini:
                decimales = len(str(increment).split(" ")[0].split(".")[1])
                tkVar.set(("{0:." + str(decimales) + "f}").format(float(tkVar.get().split(" ")[0]) - increment) + unite)
        
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
    frameBatL = ttk.Frame(frameBat, padding="5 5 5 5")
    frameBatL.grid(column=1, row=1, sticky=(N, W, E, S), padx=11)
    frameBatV = ttk.Frame(frameBat, padding="5 5 5 5")
    frameBatV.grid(column=2, row=1, sticky=E)

    genLabels(frameBatL,["Tension à 0% :","Tension à 100% :","Capacité :"])
    ttk.Label(frameBatV, textvariable=minVBat).grid(column=1, row=1, padx=5)
    Button(frameBatV, text="-", command=lambda:moins(minVBat,0.1,0," V"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=1)
    Button(frameBatV, text="+", command=lambda:plus(minVBat,0.1,100," V"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=1)
    
    ttk.Label(frameBatV, textvariable=maxVBat).grid(column=1, row=2, padx=5)
    Button(frameBatV, text="-", command=lambda:moins(maxVBat,0.1,0," V"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=2)
    Button(frameBatV, text="+", command=lambda:plus(maxVBat,0.1,100," V"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=2)

    ttk.Label(frameBatV, textvariable=capBat).grid(column=1, row=3, padx=5)
    Button(frameBatV, text="-", command=lambda:moins(capBat,1,0," Ah"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=3)
    Button(frameBatV, text="+", command=lambda:plus(capBat,1,200," Ah"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=3)
    
    #Cadre Moteur
    frameMot = ttk.Labelframe(cadre, text=' Moteur électrique ', padding="5 5 5 5")
    frameMot.grid(column=1, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    frameMotL = ttk.Frame(frameMot, padding="5 5 5 5")
    frameMotL.grid(column=1, row=1, sticky=(N, W, E, S))
    frameMotV = ttk.Frame(frameMot, padding="5 5 5 5")
    frameMotV.grid(column=2, row=1, sticky=(N, E, S))
    
    genLabels(frameMotL,["Puissance max :","Imax capteur :","Valeur capteur 0A :"])
    
    ttk.Label(frameMotV, textvariable=Pmax).grid(column=1, row=1, padx=5)
    Button(frameMotV, text="-", command=lambda:moins(Pmax,1,0," W"), width=1, repeatdelay=500, repeatinterval=25).grid(column=2, row=1)
    Button(frameMotV, text="+", command=lambda:plus(Pmax,1,3000," W"), width=1, repeatdelay=500, repeatinterval=25).grid(column=3, row=1)
    
    ttk.Label(frameMotV, textvariable=Imax).grid(column=1, row=2, padx=5)
    Button(frameMotV, text="-", command=lambda:moins(Imax,0.1,0," A"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=2)
    Button(frameMotV, text="+", command=lambda:plus(Imax,0.1,200," A"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=2)
    
    ttk.Label(frameMotV, textvariable=I0).grid(column=1, row=3, padx=5)
    Button(frameMotV, text="-", command=lambda:moins(I0,1,0," "), width=1, repeatdelay=500, repeatinterval=50).grid(column=2, row=3)
    Button(frameMotV, text="+", command=lambda:plus(I0,1,1023," "), width=1, repeatdelay=500, repeatinterval=50).grid(column=3, row=3)
    
    #Cadre Dashboard
    frameDash = ttk.Labelframe(cadre, text=' Dashboard ', padding="5 5 5 5")
    frameDash.grid(column=2, row=1, sticky=(N, W, E, S), padx=5, pady=5)
    frameDashL = ttk.Frame(frameDash, padding="5 5 5 5")
    frameDashL.grid(column=1, row=1, sticky=(N, W, E, S))
    frameDashV = ttk.Frame(frameDash, padding="5 5 5 5")
    frameDashV.grid(column=2, row=1, sticky=(N, E, S))
    
    genLabels(frameDashL,["Vitesse max :","MàJ moyennes :"])
    
    ttk.Label(frameDashV, textvariable=Vmax).grid(column=1, row=1, padx=5)
    Button(frameDashV, text="-", command=lambda:moins(Vmax,1,0," km/h"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=1)
    Button(frameDashV, text="+", command=lambda:plus(Vmax,1,200," km/h"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=1)
    
    ttk.Label(frameDashV, textvariable=majMoy).grid(column=1, row=2, padx=5)
    Button(frameDashV, text="-", command=lambda:moins(majMoy,0.1,0.1," /s"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=2)
    Button(frameDashV, text="+", command=lambda:plus(majMoy,0.1,30," /s"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=2)
    
    #Cadre Logs
    frameLog = ttk.Labelframe(cadre, text=' Logs ', padding="5 5 5 5")
    frameLog.grid(column=2, row=2, sticky=(N, W, E, S), padx=5, pady=5)
    frameLogL = ttk.Frame(frameLog, padding="5 5 5 5")
    frameLogL.grid(column=1, row=1, sticky=(N, W, E, S), padx=1)
    frameLogV = ttk.Frame(frameLog, padding="5 5 5 5")
    frameLogV.grid(column=2, row=1, sticky=(N, E, S))
    
    genLabels(frameLogL,["Mise à jour relevés :"])
    
    ttk.Label(frameLogV, textvariable=tempo).grid(column=1, row=1, padx=5)
    Button(frameLogV, text="-", command=lambda:moins(tempo,0.1,0.1," /s"), width=1, repeatdelay=500, repeatinterval=100).grid(column=2, row=1)
    Button(frameLogV, text="+", command=lambda:plus(tempo,0.1,30," /s"), width=1, repeatdelay=500, repeatinterval=100).grid(column=3, row=1)
    
    #Cadre bouton
    frameBouton = ttk.Frame(cadre)
    frameBouton.grid(column=1, row=3, columnspan=2)
    ttk.Button(frameBouton, text="Valider", command=majParam).grid(column=1, row=1, pady=5)
    ttk.Button(frameBouton, text="Réinitialiser", command=razParam).grid(column=2, row=1, pady=5)
    
    fenetre.mainloop()
    

if __name__ == '__main__':
    
    interfaceParametres()

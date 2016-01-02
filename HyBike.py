#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  HyBike.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#
#

from tkinter import *
from tkinter import ttk

from moyennes import *
from fonctionsData import *
from configuration import *
from getData import *


def HyBike(changeParam, ser):
    #   Interface principale (Dashboard) du programme OpenHyBike
    # 
    #   @param : 
    #       changeParam : booléen permettant de savoir si un changement de paramètre à eu lieu
    #       ser : objet contenant la connection au port série (connection avec Arduino)
    #
    #   
    
    
    def startData(*args):
        tkObj = {"lbatt":lbatt,"lMoyConso":lMoyConso}
        moyennes = {"conso":conso,"vite":vite}
        getData(ser, fenetre, tkVars, tkObj, moyennes, params)

    def stopLog(*args):
        tkVars["logON"].set("False")
    
    def startLog(*args):
        tkVars["logON"].set("True")

    def RAZ(*args):
        remiseAZ(conso,vite,tkVars["moyenneConso"],tkVars["moyenneVitesse"])
    
    def modifParam(*args):
        changeParam[0] = True
        fenetre.destroy()


    """Chargement des paramètres"""
    params = lireConf()

    """Définition des variables"""
    conso = {"moy":0,"nb":0,"i":0}  #serie de moyenne des consommations
    vite = {"moy":0,"nb":0,"i":0}   #serie de moyenne des vitesses

    """Interface"""
    fenetre = Tk()
    fenetre.title("Dashboard")
    fenetre.geometry("800x480")


    """Variables"""
    tkVars = creerVarTK()


    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=0, row=0, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)

    #Cadre Accélérateur
    frameAcc = ttk.Labelframe(cadre, text=' Accélérateur ', padding="5 5 5 5")
    frameAcc.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=2, columnspan=5, padx=5, pady=5)

    ttk.Progressbar(frameAcc, orient=HORIZONTAL, length=400, mode='determinate', variable=tkVars["accelerateurValeur"], maximum=100).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(frameAcc, textvariable=tkVars["valeurAccStr"]).grid(column=1, row=2)

    #Cadre Frein
    frameFrein = ttk.Labelframe(cadre, text=' Frein ', padding="5 5 5 5")
    frameFrein.grid(column=1, row=3, sticky=(N, W, E, S), rowspan=2, columnspan=5, padx=5, pady=5)

    ttk.Progressbar(frameFrein, orient=HORIZONTAL, length=400, mode='determinate', variable=tkVars["freinValeur"], maximum=100).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(frameFrein, textvariable=tkVars["valeurFreinStr"]).grid(column=1, row=2)

    #Cadre Batterie
    frameBatt = ttk.LabelFrame(cadre, text=' Batterie ', padding="5 5 5 5")
    frameBatt.grid(column=7, row=1, sticky=(N, W, E, S), rowspan = 4, columnspan = 2, padx=5, pady=5)

    ttk.Progressbar(frameBatt, orient=VERTICAL, length=120, mode='determinate', variable=tkVars["batterieValeur"], maximum=100).grid(column=1, row=1, rowspan=3, sticky=(W, E), padx=5)
    lbatt = ttk.Label(frameBatt, textvariable=tkVars["valeurBattStr"])
    lbatt.grid(column=2, row=1, padx=5)
    ttk.Label(frameBatt, textvariable=tkVars["voltageBattStr"]).grid(column=2, row=2, padx=5)
    ttk.Label(frameBatt, textvariable=tkVars["energieBattStr"]).grid(column=2, row=3, padx=5)

    #Cadre Consommation
    frameConso = ttk.LabelFrame(cadre, text=' Consommation ', padding="5 5 5 5")
    frameConso.grid(column=9, row=1, sticky=(N, W, E, S), rowspan = 4, columnspan = 4, padx=5, pady=5)

    ttk.Label(frameConso, text="Recharge").grid(column=1, row=1, padx=5)
    ttk.Label(frameConso, textvariable=tkVars["valeurPuisProdStr"], foreground="green").grid(column=1, row=3, padx=5)
    ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=tkVars["puissanceValeurProd"], maximum=params["Pmax"]).grid(column=2, row=1, rowspan=3, sticky=(W, E), padx=5)
    ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=tkVars["puissanceValeurConso"], maximum=params["Pmax"]).grid(column=3, row=1, rowspan=3, sticky=(W, E), padx=5)
    ttk.Label(frameConso, text="Décharge").grid(column=4, row=1, padx=5)
    ttk.Label(frameConso, textvariable=tkVars["valeurPuisConsoStr"], foreground="red").grid(column=4, row=3, padx=5)
    Fmoy = ttk.Frame(frameConso)
    Fmoy.grid(column=1, row=4, columnspan=4)
    lMoyConso = ttk.Label(Fmoy, textvariable=tkVars["moyenneConso"])
    lMoyConso.grid(column=1, row=1, padx=5, pady=5)
    ttk.Label(Fmoy, textvariable=tkVars["estimationBatt"]).grid(column=2, row=1, padx=5, pady=5)

    #Cadre Vitesse
    frameVitesse = ttk.LabelFrame(cadre, text=' Vitesse ', padding="5 5 5 5")
    frameVitesse.grid(column=1, row=5, sticky=(N, W, E, S), columnspan = 13, padx=5, pady=5)

    Fvit = ttk.Frame(frameVitesse)
    Fvit.grid(column=1, row=1, columnspan=13)
    ttk.Label(Fvit, textvariable=tkVars["valeurVitesseStr"]).grid(column=1, row=1, padx=5, pady=5)
    ttk.Progressbar(frameVitesse, orient=HORIZONTAL, length=740, mode='determinate', variable=tkVars["vitesseValeur"], maximum=params["Vmax"]).grid(column=1, row=2, columnspan=13, sticky=(W, E), pady=5, padx=5)
    Fvit2 = ttk.Frame(frameVitesse)
    Fvit2.grid(column=1, row=3, columnspan=13)
    ttk.Label(Fvit2, textvariable=tkVars["moyenneVitesse"]).grid(column=1, row=1, padx=25, pady=5)
    ttk.Label(Fvit2, textvariable=tkVars["estimationVitesse"]).grid(column=2, row=1, padx=25, pady=5)


    #Cadre Boutons
    Fbouton = ttk.Frame(cadre)
    Fbouton.grid(column=1, row=6, columnspan=13)
    ttk.Button(Fbouton, text="Start", command=startLog).grid(column=2, row=1, pady=5)
    ttk.Button(Fbouton, text="Stop", command=stopLog).grid(column=3, row=1, pady=5)
    ttk.Button(Fbouton, text="RAZ", command=RAZ).grid(column=4, row=1, pady=5)
    ttk.Button(Fbouton, text="Paramètres", command=modifParam).grid(column=5, row=1, pady=5)
    ttk.Button(Fbouton, text="Quitter", command=fenetre.destroy).grid(column=6, row=1, pady=5)

    fenetre.after(0, startData)   #Démarre l'affichage des données dès le lancement de la fenêtre
    fenetre.mainloop()

if __name__ == '__main__':
    
    exit()

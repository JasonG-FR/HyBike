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
from time import sleep
from random import randint
import serial

from fonctionsArduino import *
from fonctionsData import *
from moyennes import *
from formatH import *
from fonctionsLogs import *
from configuration import *
from interfaceParametres import *


def HyBike(changeParam):

    """Chargement des paramètres"""
    params = lireConf()

    """Définition des variables"""
    conso = {"moy":0,"nb":0,"i":0}  #serie de moyenne des consommations
    vite = {"moy":0,"nb":0,"i":0}   #serie de moyenne des vitesses

    def updateData(dataTab, data, fichier=False, tpsConsigne=0, tempo=1, donnees=0, *args):
        #Vérifier si le flux est complet, sinon attendre qu'il n'y ait plus d'erreurs
        try:
            """Conversion des données Arduino"""
            convArduino(dataTab, data)
    
            """Mise à jour des variables de l'interface"""
            ##Accélérateur
            majProgressBar(data["valAcc"],accelerateurValeur,valeurAccStr)
    
            ##Frein
            majProgressBar(data["valFrein"],freinValeur,valeurFreinStr)
    
            ##Batterie
            majProgressBar(data["valBatt"],batterieValeur,valeurBattStr)
            Tension = data["valBatt"]*(params["maxVBat"]-params["minVBat"])/100.+params["minVBat"]
            voltageBattStr.set("{0:.2f}".format(Tension) + " V")
            
            majCouleur(data["valBatt"],lbatt,"green",30,"orange",10,"red")
            
            """Le choix de cet algorithme de calcul est à vérifier (cycle de décharge non linéaire, estimation energie à calibrer) -> cf fichier ODC"""
            energie = params["capBat"]*params["maxVBat"]*data["valBatt"]/100
            energieBattStr.set("{0:.2f}".format(energie) + " Wh")
    
            ##Consommation
            Intensite = convBinNumCentre(params["I0"],data["valIntensite"],params["Imax"])
            puissance = Tension*Intensite
                
            if puissance > 0:
                #Décharge
                majProgressBar(puissance,puissanceValeurConso,valeurPuisConsoStr,0,"W")
                majProgressBar(0,puissanceValeurProd,valeurPuisProdStr,0,"W")
                
            elif puissance < 0:
                #Charge
                majProgressBar(0,puissanceValeurConso,valeurPuisConsoStr,0,"W")
                majProgressBar(-1*puissance,puissanceValeurProd,valeurPuisProdStr,0,"W")
                
            else:
                #Arrêt
                majProgressBar(0,puissanceValeurConso,valeurPuisConsoStr,0,"W")
                majProgressBar(0,puissanceValeurProd,valeurPuisProdStr,0,"W")
            
            moyenneDynamique(conso,puissance,params["majMoy"])
            moyenneConso.set("{0:.0f}".format(conso["moy"]) + " W")
            majCouleur(conso["moy"],lMoyConso,"red",0,"green")
            
            if conso["moy"] > 0:
                autonomie = energie/conso["moy"]
                estimationBatt.set("~ " + formatH(autonomie))
            else:
                autonomie = -1
                estimationBatt.set("N/A")
        
            ##Vitesse
            vitesse = data["valVitesse"]*params["Vmax"]/100
            vitesseValeur.set(vitesse)
            valeurVitesseStr.set("{0:.0f}".format(vitesse) + " km/h   <=>   "+"{0:.1f}".format(vitesse*10/36.) + " m/s")
            moyenneDynamique(vite,vitesse,params["majMoy"])
            moyenneVitesse.set("Vitesse moyenne : " + "{0:.1f}".format(vite["moy"]) + " km/h")
            if autonomie < 0:
                estimationVitesse.set("Autonomie restante : N/A")
            else:
                estimationVitesse.set("Autonomie restante : ~ " + "{0:.0f}".format(vite["moy"]*autonomie) + " km")
            
            """Mise à jour du log si actif"""
            if fichier != False:
                #[tps,acc,frein,ubat,imot,vit]
                donnees[1] = str(accelerateurValeur.get())
                donnees[2] = str(freinValeur.get())
                donnees[3] = "{0:.2f}".format(Tension)
                donnees[4] = "{0:.2f}".format(Intensite)
                donnees[5] = "{0:.1f}".format(vitesseValeur.get())
                logSession(fichier,donnees,tpsConsigne,tempo)
            
        except ValueError:
            #Pause de 10ms
            sleep(0.01)
        except IndexError:
            #Pause de 10ms
            sleep(0.01)

    def getData(*args):
    
        data = {}
        tpsConsigne = [0]
        fichier = 0
    
        #Flush du tampon d'Arduino
        ser.flushInput()
    
        while(True):
            #Lecture des données issues d'Arduino
            dataTab = decodageArduino(ser)
        
            #Mise à jour des variables et de l'affichage
            if logON.get():
                #On crée le fichier s'il n'existe pas
                if fichier == 0:
                    
                    fichier = open(nomLog(),"w")
                    #[tps,acc,frein,ubat,imot,vit]
                    donnees = ["0","0","0","0","0","0"]
        
                updateData(dataTab, data, fichier, tpsConsigne, params["tempo"], donnees)
            else:
                #On ferme le fichier s'il est ouvert
                if fichier != 0:
                    fichier.close()
                    fichier = 0
            
                updateData(dataTab, data)
        
            try:
                fenetre.update()
            except TclError:
                break
    
        try:
            fenetre.update()
        except TclError:
            return 1

    def stopLog(*args):
        logON.set("False")
    
    def startLog(*args):
        logON.set("True")

    def RAZ(*args):
        remiseAZ(conso,vite,moyenneConso,moyenneVitesse)
    
    def modifParam(*args):
        changeParam[0] = True
        fenetre.destroy()

    """Interface"""
    fenetre = Tk()
    fenetre.title("Dashboard")
    fenetre.geometry("800x480")


    """Variables"""
    
    #Globales
    logON = BooleanVar()
    logON.set("False")

    #Accélérateur
    accelerateurValeur = IntVar()
    valeurAccStr = StringVar()

    #Frein
    freinValeur = IntVar()
    valeurFreinStr = StringVar()

    #Batterie
    batterieValeur = IntVar()
    valeurBattStr = StringVar()
    voltageBattStr = StringVar()
    energieBattStr = StringVar()

    #Consommation
    puissanceValeurConso = DoubleVar()
    puissanceValeurProd = DoubleVar()
    valeurPuisConsoStr = StringVar()
    valeurPuisProdStr = StringVar()
    moyenneConso = StringVar()
    estimationBatt = StringVar()

    #Vitesse
    vitesseValeur = DoubleVar()
    valeurVitesseStr = StringVar()
    moyenneVitesse = StringVar()
    estimationVitesse = StringVar()


    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=0, row=0, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)

    #Cadre Accélérateur
    frameAcc = ttk.Labelframe(cadre, text=' Accélérateur ', padding="5 5 5 5")
    frameAcc.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=2, columnspan=5, padx=5, pady=5)

    ttk.Progressbar(frameAcc, orient=HORIZONTAL, length=400, mode='determinate', variable=accelerateurValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(frameAcc, textvariable=valeurAccStr).grid(column=1, row=2)

    #Cadre Frein
    frameFrein = ttk.Labelframe(cadre, text=' Frein ', padding="5 5 5 5")
    frameFrein.grid(column=1, row=3, sticky=(N, W, E, S), rowspan=2, columnspan=5, padx=5, pady=5)

    ttk.Progressbar(frameFrein, orient=HORIZONTAL, length=400, mode='determinate', variable=freinValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(frameFrein, textvariable=valeurFreinStr).grid(column=1, row=2)

    #Cadre Batterie
    frameBatt = ttk.LabelFrame(cadre, text=' Batterie ', padding="5 5 5 5")
    frameBatt.grid(column=7, row=1, sticky=(N, W, E, S), rowspan = 4, columnspan = 2, padx=5, pady=5)

    ttk.Progressbar(frameBatt, orient=VERTICAL, length=120, mode='determinate', variable=batterieValeur, maximum=100).grid(column=1, row=1, rowspan=3, sticky=(W, E), padx=5)
    lbatt = ttk.Label(frameBatt, textvariable=valeurBattStr)
    lbatt.grid(column=2, row=1, padx=5)
    ttk.Label(frameBatt, textvariable=voltageBattStr).grid(column=2, row=2, padx=5)
    ttk.Label(frameBatt, textvariable=energieBattStr).grid(column=2, row=3, padx=5)

    #Cadre Consommation
    frameConso = ttk.LabelFrame(cadre, text=' Consommation ', padding="5 5 5 5")
    frameConso.grid(column=9, row=1, sticky=(N, W, E, S), rowspan = 4, columnspan = 4, padx=5, pady=5)

    ttk.Label(frameConso, text="Recharge").grid(column=1, row=1, padx=5)
    ttk.Label(frameConso, textvariable=valeurPuisProdStr, foreground="green").grid(column=1, row=3, padx=5)
    ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurProd, maximum=params["Pmax"]).grid(column=2, row=1, rowspan=3, sticky=(W, E), padx=5)
    ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurConso, maximum=params["Pmax"]).grid(column=3, row=1, rowspan=3, sticky=(W, E), padx=5)
    ttk.Label(frameConso, text="Décharge").grid(column=4, row=1, padx=5)
    ttk.Label(frameConso, textvariable=valeurPuisConsoStr, foreground="red").grid(column=4, row=3, padx=5)
    Fmoy = ttk.Frame(frameConso)
    Fmoy.grid(column=1, row=4, columnspan=4)
    lMoyConso = ttk.Label(Fmoy, textvariable=moyenneConso)
    lMoyConso.grid(column=1, row=1, padx=5, pady=5)
    ttk.Label(Fmoy, textvariable=estimationBatt).grid(column=2, row=1, padx=5, pady=5)

    #Cadre Vitesse
    frameVitesse = ttk.LabelFrame(cadre, text=' Vitesse ', padding="5 5 5 5")
    frameVitesse.grid(column=1, row=5, sticky=(N, W, E, S), columnspan = 13, padx=5, pady=5)

    Fvit = ttk.Frame(frameVitesse)
    Fvit.grid(column=1, row=1, columnspan=13)
    ttk.Label(Fvit, textvariable=valeurVitesseStr).grid(column=1, row=1, padx=5, pady=5)
    ttk.Progressbar(frameVitesse, orient=HORIZONTAL, length=740, mode='determinate', variable=vitesseValeur, maximum=params["Vmax"]).grid(column=1, row=2, columnspan=13, sticky=(W, E), pady=5, padx=5)
    Fvit2 = ttk.Frame(frameVitesse)
    Fvit2.grid(column=1, row=3, columnspan=13)
    ttk.Label(Fvit2, textvariable=moyenneVitesse).grid(column=1, row=1, padx=25, pady=5)
    ttk.Label(Fvit2, textvariable=estimationVitesse).grid(column=2, row=1, padx=25, pady=5)


    #Cadre Boutons
    Fbouton = ttk.Frame(cadre)
    Fbouton.grid(column=1, row=6, columnspan=13)
    ttk.Button(Fbouton, text="Start", command=startLog).grid(column=2, row=1, pady=5)
    ttk.Button(Fbouton, text="Stop", command=stopLog).grid(column=3, row=1, pady=5)
    ttk.Button(Fbouton, text="RAZ", command=RAZ).grid(column=4, row=1, pady=5)
    ttk.Button(Fbouton, text="Paramètres", command=modifParam).grid(column=5, row=1, pady=5)
    ttk.Button(Fbouton, text="Quitter", command=fenetre.destroy).grid(column=6, row=1, pady=5)

    fenetre.after(0, getData)   #Démarre l'affichage des données dès le lancement de la fenêtre
    fenetre.mainloop()

if __name__ == '__main__':
    
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600)
        ser.readline()
    except serial.serialutil.SerialException:
        print("Arduino non connecté!")
        exit()
        
    changeParam = [False]
    
    #On lance l'interface principale
    HyBike(changeParam)
    
    #Tant qu'on veux changer les paramètres
    while changeParam[0]:
        #On lance l'interface des paramètres
        interfaceParametres()
        changeParam[0] = False
        #Puis on relance l'interface principale
        HyBike(changeParam)

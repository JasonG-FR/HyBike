#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  HyBrike.py
#  
#  Copyright 2015 Jason Gombert <jason.gombert@gmail.com>
#
#

from tkinter import *
from tkinter import ttk
from time import sleep
import serial

from decodageArduino import *
from moyenneDynamique import *
from formatH import *

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.readline()

"""Paramètres physiques"""
minVBat = 10.8  #Batterie à 0%
maxVBat = 13.6  #Batterie à 100%
capBat = 12     #Capacité en Ah
Pmax = 1500     #Puissance electrique maximale du moteur
Imax = 150.     #Adapter en fonction du capteur (valeur de Imax en A pour 1023 renvoyé par le capteur)
I0 = 512        #Valeur envoyée par le capteur pour I = 0A

"""Variables"""
conso = {"moy":0,"nb":0,"i":0}  #serie de moyenne de consommation
majMoy = 3                      #Taux d'actualisation des moyennes (1 pour 30fps, 30 pour 1fps)

def updateData(dataTab, data, *args):
    
    #Vérifier si le flux est complet, sinon attendre qu'il n'y ait plus d'erreurs
        try:
            #Format Arduino : acc;frein;batt;intensité
            data["valAcc"] = int(int(dataTab[0])/1023*100)
            data["valFrein"] = int(int(dataTab[1])/1023*100)
            data["valBatt"] = int(int(dataTab[2])/1023*100)
            data["valIntensite"] = int(dataTab[3])  
        
            """Mise à jour des variables de l'interface"""
            ##Accélérateur
            accelerateurValeur.set(data["valAcc"])
            valeurAccStr.set(str(data["valAcc"]) + " %")
        
            ##Frein
            freinValeur.set(data["valFrein"])
            valeurFreinStr.set(str(data["valFrein"]) + " %")
        
            ##Batterie
            Tension = data["valBatt"]*(maxVBat-minVBat)/100.+minVBat
            batterieValeur.set(data["valBatt"])
            valeurBattStr.set(str(data["valBatt"]) + " %")
            voltageBattStr.set("{0:.2f}".format(Tension) + " V")
            
            #Le choix de cet algorithme de calcul est à vérifier (cycle de décharge non linéaire, estimation energie à calibrer) -> cf fichier ODC
            energie = capBat*maxVBat*data["valBatt"]/100
            
            energieBattStr.set("{0:.2f}".format(energie) + " Wh")
            
        
            ##Consommation
            if(data["valIntensite"] > I0):
                #Décharge
                tauxEch = Imax/(1023-I0)            #Echantillonnage
                Ipositif = data["valIntensite"]-I0  #On décale le zéro de I0 à 0
                puissance = Tension*Ipositif*tauxEch
                puissanceValeurConso.set(puissance)
                puissanceValeurProd.set(0)
                valeurPuisConsoStr.set("{0:.0f}".format(puissance) + " W")
                valeurPuisProdStr.set("0 W")
                moyenneDynamique(conso,puissance,majMoy)
                
            elif(data["valIntensite"] < I0):
                #Charge
                tauxEch = Imax/I0            #Echantillonnage
                puissance = Tension*(data["valIntensite"]-I0)*tauxEch*-1
                puissanceValeurConso.set(0)
                puissanceValeurProd.set(puissance)
                valeurPuisConsoStr.set("0 W")
                valeurPuisProdStr.set("{0:.0f}".format(puissance) + " W")
                moyenneDynamique(conso,puissance*-1,majMoy)
                
            else:
                #Arrêt
                puissanceValeurConso.set(0)
                puissanceValeurProd.set(0)
                valeurPuisConsoStr.set("0 W")
                valeurPuisProdStr.set("0 W")
                moyenneDynamique(conso,0,majMoy)
            
            moyenneConso.set("{0:.0f}".format(conso["moy"]) + " W")
            try:
                autonomie = energie/conso["moy"]
                if autonomie < 0:
                    estimationBatt.set("N/A")
                else:
                    estimationBatt.set("~ " + formatH(autonomie))
            except ZeroDivisionError:
                estimationBatt.set("N/A")
            
        
        except ValueError:
            #Pause de 10ms
            sleep(0.01)
        except IndexError:
            #Pause de 10ms
            sleep(0.01)

def getData(*args):
    
    data = {}
    while(True):
        """Lecture des données issues d'Arduino"""
        dataTab = decodageArduino(ser)
        
        """Mise à jour des variables et de l'affichage"""
        updateData(dataTab, data)
        
        try:
            fenetre.update()
        except TclError:
            break


"""Interface"""
fenetre = Tk()
fenetre.title("Dashboard")
fenetre.geometry("840x480")


"""Variables"""
#Accélérateur
accelerateurValeur = IntVar()
valeurAccStr = StringVar()
valeurAccStr.set("")

#Frein
freinValeur = IntVar()
valeurFreinStr = StringVar()
valeurFreinStr.set("")

#Batterie
batterieValeur = IntVar()
valeurBattStr = StringVar()
voltageBattStr = StringVar()
energieBattStr = StringVar()
valeurBattStr.set("")
voltageBattStr.set("")
energieBattStr.set("")

#Consommation
puissanceValeurConso = DoubleVar()
puissanceValeurProd = DoubleVar()
valeurPuisConsoStr = StringVar()
valeurPuisProdStr = StringVar()
moyenneConso = StringVar()
estimationBatt = StringVar()

valeurPuisConsoStr.set("")
valeurPuisProdStr.set("")
moyenneConso.set("")
estimationBatt.set("")


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
ttk.Label(frameBatt, textvariable=valeurBattStr).grid(column=2, row=1, padx=5)
ttk.Label(frameBatt, textvariable=voltageBattStr).grid(column=2, row=2, padx=5)
ttk.Label(frameBatt, textvariable=energieBattStr).grid(column=2, row=3, padx=5)

#Cadre Consommation
frameConso = ttk.LabelFrame(cadre, text=' Consommation ', padding="5 5 5 5")
frameConso.grid(column=9, row=1, sticky=(N, W, E, S), rowspan = 4, columnspan = 4, padx=5, pady=5)

ttk.Label(frameConso, text="Recharge").grid(column=1, row=1, padx=5)
ttk.Label(frameConso, textvariable=valeurPuisProdStr).grid(column=1, row=3, padx=5)
ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurProd, maximum=Pmax).grid(column=2, row=1, rowspan=3, sticky=(W, E), padx=5)
ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurConso, maximum=Pmax).grid(column=3, row=1, rowspan=3, sticky=(W, E), padx=5)
ttk.Label(frameConso, text="Décharge").grid(column=4, row=1, padx=5)
ttk.Label(frameConso, textvariable=valeurPuisConsoStr).grid(column=4, row=3, padx=5)
Fmoy = ttk.Frame(frameConso)
Fmoy.grid(column=1, row=4, columnspan=4)
ttk.Label(Fmoy, textvariable=moyenneConso).grid(column=1, row=1, padx=5, pady=5)
ttk.Label(Fmoy, textvariable=estimationBatt).grid(column=2, row=1, padx=5, pady=5)


#Cadre Boutons
Fbouton = ttk.Frame(cadre)
Fbouton.grid(column=1, row=5, columnspan=13)
ttk.Button(Fbouton, text="Start", command=getData).grid(column=2, row=1, pady=5)
ttk.Button(Fbouton, text="Quitter", command=fenetre.destroy).grid(column=3, row=1, pady=5)

fenetre.mainloop()

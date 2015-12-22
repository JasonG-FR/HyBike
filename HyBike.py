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

try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.readline()
except serial.serialutil.SerialException:
    print("Arduino non connecté!")
    exit()

"""Paramètres physiques"""
minVBat = 10.8*3    #Batterie à 0%
maxVBat = 13.6*3    #Batterie à 100%
capBat = 12         #Capacité en Ah
Pmax = 1500         #Puissance electrique maximale du moteur
Imax = 150./3       #Adapter en fonction du capteur (valeur de Imax en A pour 1023 renvoyé par le capteur)
I0 = 512            #Valeur envoyée par le capteur pour I = 0A
Vmax = 100          #Vitesse maximale en km/h

"""Variables"""
conso = {"moy":0,"nb":0,"i":0}  #serie de moyenne des consommations
vite = {"moy":0,"nb":0,"i":0}   #serie de moyenne des vitesses
majMoy = 3                      #Taux d'actualisation des moyennes (1 pour 30fps, 30 pour 1fps)

def colorer(objet,couleur):
    try:
        objet.configure(foreground=couleur)
    except TclError:
        exit()

def updateData(dataTab, data, *args):
    
    #Vérifier si le flux est complet, sinon attendre qu'il n'y ait plus d'erreurs
        try:
            #Format Arduino : acc;frein;batt;intensité;vitesse
            data["valAcc"] = int(int(dataTab[0])/1023*100)
            data["valFrein"] = int(int(dataTab[1])/1023*100)
            data["valBatt"] = int(int(dataTab[2])/1023*100)
            data["valIntensite"] = int(dataTab[3])
            data["valVitesse"] = int(dataTab[4])/1023.*100
        
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
            if data["valBatt"] > 30:
                colorer(lbatt,"green")
            elif data["valBatt"] > 10:
                colorer(lbatt,"orange")
            else:
                colorer(lbatt,"red")
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
            if conso["moy"] > 0:
                colorer(lMoyConso,"red")
                autonomie = energie/conso["moy"]
                estimationBatt.set("~ " + formatH(autonomie))
            else:
                colorer(lMoyConso,"green")
                autonomie = -1
                estimationBatt.set("N/A")
            
            ##Vitesse
            vitesse = data["valVitesse"]*Vmax/100
            vitesseValeur.set(vitesse)
            valeurVitesseStr.set("{0:.0f}".format(vitesse) + " km/h   <=>   "+"{0:.1f}".format(vitesse*10/36.) + " m/s")
            moyenneDynamique(vite,vitesse,majMoy)
            moyenneVitesse.set("Vitesse moyenne : " + "{0:.1f}".format(vite["moy"]) + " km/h")
            if autonomie < 0:
                estimationVitesse.set("Autonomie restante : N/A")
            else:
                estimationVitesse.set("Autonomie restante : ~ " + "{0:.0f}".format(vite["moy"]*autonomie) + " km")
            
        
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
fenetre.geometry("800x480")


"""Variables"""
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
ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurProd, maximum=Pmax).grid(column=2, row=1, rowspan=3, sticky=(W, E), padx=5)
ttk.Progressbar(frameConso, orient=VERTICAL, length=100, mode='determinate', variable=puissanceValeurConso, maximum=Pmax).grid(column=3, row=1, rowspan=3, sticky=(W, E), padx=5)
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
ttk.Progressbar(frameVitesse, orient=HORIZONTAL, length=740, mode='determinate', variable=vitesseValeur, maximum=Vmax).grid(column=1, row=2, columnspan=13, sticky=(W, E), pady=5, padx=5)
Fvit2 = ttk.Frame(frameVitesse)
Fvit2.grid(column=1, row=3, columnspan=13)
ttk.Label(Fvit2, textvariable=moyenneVitesse).grid(column=1, row=1, padx=25, pady=5)
ttk.Label(Fvit2, textvariable=estimationVitesse).grid(column=2, row=1, padx=25, pady=5)


#Cadre Boutons
Fbouton = ttk.Frame(cadre)
Fbouton.grid(column=1, row=6, columnspan=13)
ttk.Button(Fbouton, text="Start", command=getData).grid(column=2, row=1, pady=5)
ttk.Button(Fbouton, text="Quitter", command=fenetre.destroy).grid(column=3, row=1, pady=5)

fenetre.mainloop()

#!/usr/bin/env python2
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

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.readline()

"""Paramètres physiques"""
minVBat = 10.8  #Batterie à 0%
maxVBat = 13.6  #Batterie à 100%
capBat = 12     #Capacité en Ah

def getData(*args):
    
    while(True):
        """Lecture des données issues d'Arduino"""
        #Format de donnée csv avec ";" comme séparateur : le format recu est : b'0000;2222;2222\n'
        dataRaw = str(ser.readline()) 
        
        #On enlève le premier caractère (b pour signaler une variable octale) et les caractères spéciaux (' et \n)
        dataRaw = dataRaw[1:]
        dataRaw = dataRaw.replace("'","")
        dataRaw = dataRaw.replace("\\n","")
        
        """Séparation des variables, traitement et insertion dans un dictionnaire pour être plus lisible"""
        dataTab = dataRaw.split(";")
        data = {}
        
        #Vérifie si le flux est complet, sinon attendre qu'il le soit
        try:
            #Format Arduino : acc;frein;batt
            data["valAcc"] = int(int(dataTab[0])/1023*100)
            data["valFrein"] = int(int(dataTab[1])/1023*100)
            data["valBatt"] = int(int(dataTab[2])/1023*100)
        
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
            energieBattStr.set("{0:.2f}".format(capBat*maxVBat*data["valBatt"]/100) + " Wh")
            #Le choix de ces algorithmes de calcul est à vérifier (cycle de décharge non linéaire, estimation energie à calibrer) -> cf fichier ODC
         
        
            #Mise à jour affichage
            try:
                fenetre.update()
            except TclError:
                break
        except ValueError:
            #Pause de 10ms
            sleep(0.01)
        except IndexError:
            #Pause de 10ms
            sleep(0.01)

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
frameBatt.grid(column=7, row=1, sticky=(N, W, E, S), rowspan = 4, padx=5, pady=5)

ttk.Progressbar(frameBatt, orient=VERTICAL, length=100, mode='determinate', variable=batterieValeur, maximum=100).grid(column=1, row=1, rowspan=3, sticky=(W, E), padx=5)
ttk.Label(frameBatt, textvariable=valeurBattStr).grid(column=2, row=1, padx=5)
ttk.Label(frameBatt, textvariable=voltageBattStr).grid(column=2, row=2, padx=5)
ttk.Label(frameBatt, textvariable=energieBattStr).grid(column=2, row=3, padx=5)

#Cadre Boutons
Fbouton = ttk.Frame(cadre)
Fbouton.grid(column=1, row=5, columnspan=7)
ttk.Button(Fbouton, text="Start", command=getData).grid(column=2, row=1, pady=5)
ttk.Button(Fbouton, text="Quitter", command=fenetre.destroy).grid(column=3, row=1, pady=5)

fenetre.mainloop()

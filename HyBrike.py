#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

#Paramètres physiques
minVBat = 10.8  #Batterie à 0%
maxVBat = 13.6  #Batterie à 100%

def getData(*args):
    
    #On élimine la première lecture qui est incomplète
    ser.readline()
    sleep(0.1)
    
    while(True):
        #Lecture des données issues d'Arduino
        dataRaw = str(ser.readline()) #Format de donnée csv avec ";" comme séparateur : le format recu est : b'0000;2222;2222\n'
        #On enlève le premier caractère (b pour signaler une variable octale) et les caractères spéciaux (' et \n)
        dataRaw = dataRaw[1:]
        dataRaw = dataRaw.replace("'","")
        dataRaw = dataRaw.replace("\\n","")
        #Séparation des variables, traitement et insertion dans un dictionnaire pour être plus lisible
        #Format Arduino : acc;frein;batt
        dataTab = dataRaw.split(";")
        data = {}
        data["valAcc"] = int(int(dataTab[0])/1023*100)
        data["valFrein"] = int(int(dataTab[1])/1023*100)
        data["valBatt"] = int(int(dataTab[2])/1023*100)
        
        #Mise à jour des variables de l'interface :
        
        ##Accélérateur
        accelerateurValeur.set(data["valAcc"])
        valeurAccStr.set(str(data["valAcc"]) + " %")
        
        ##Frein
        freinValeur.set(data["valFrein"])
        valeurFreinStr.set(str(data["valFrein"]) + " %")
        
        ##Batterie
        batterieValeur.set(data["valBatt"])
        valeurBattStr.set(str(data["valBatt"]) + " %")
        voltageBattStr.set("{0:.2f}".format(data["valBatt"]*(maxVBat-minVBat)/100.+minVBat) + " V")
        
        #Mise à jour affichage
        fenetre.update()

fenetre = Tk()
fenetre.title("Dashboard")

accelerateurValeur = IntVar()
valeurAccStr = StringVar()
valeurAccStr.set("N/A")

freinValeur = IntVar()
valeurFreinStr = StringVar()
valeurFreinStr.set("N/A")

batterieValeur = IntVar()
valeurBattStr = StringVar()
voltageBattStr = StringVar()
valeurBattStr.set("N/A")
voltageBattStr.set("N/A")

cadre = ttk.Frame(fenetre, padding="3 3 12 12")
cadre.grid(column=0, row=0, sticky=(N, W, E, S))
cadre.columnconfigure(0, weight=1)
cadre.rowconfigure(0, weight=1)

#Cadre Accélérateur
frameAcc = ttk.Labelframe(cadre, text='Accélérateur', padding="3 3 12 12")
frameAcc.grid(column=1, row=1, sticky=(N, W, E, S), rowspan=2, columnspan=5)

ttk.Progressbar(frameAcc, orient=HORIZONTAL, length=400, mode='determinate', variable=accelerateurValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
ttk.Label(frameAcc, textvariable=valeurAccStr).grid(column=1, row=2)

#Cadre Frein
frameFrein = ttk.Labelframe(cadre, text='Frein', padding="3 3 12 12")
frameFrein.grid(column=1, row=3, sticky=(N, W, E, S), rowspan=2, columnspan=5)

ttk.Progressbar(frameFrein, orient=HORIZONTAL, length=400, mode='determinate', variable=freinValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
ttk.Label(frameFrein, textvariable=valeurFreinStr).grid(column=1, row=2)

#Cadre Batterie
frameBatt = ttk.Labelframe(cadre, text='Batterie', padding="3 3 12 12")
frameBatt.grid(column=7, row=1, sticky=(N, W, E, S), rowspan = 4)

ttk.Progressbar(frameBatt, orient=VERTICAL, length=100, mode='determinate', variable=batterieValeur, maximum=100).grid(column=1, row=1, rowspan=4, sticky=(W, E))
ttk.Label(frameBatt, textvariable=valeurBattStr).grid(column=2, row=2, sticky=(E), padx=5)
ttk.Label(frameBatt, textvariable=voltageBattStr).grid(column=2, row=3, sticky=(E), padx=5)

ttk.Button(cadre, text="start", command=getData).grid(column=3, row=5)
ttk.Button(cadre, text="quitter", command=fenetre.destroy).grid(column=4, row=5)

fenetre.mainloop()

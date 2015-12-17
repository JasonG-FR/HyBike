#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def getData(*args):
    while(True):
        #Lecture des données issues d'Arduino
        dataRaw = str(ser.readline()) #Format de donnée csv avec ";" comme séparateur : le format recu est : b'0000;2222;2222\n'
        #On enlève le premier caractère (b pour signaler une variable octale) et les caractères spéciaux (' et \n)
        dataRaw = dataRaw[1:]
        dataRaw = dataRaw.replace("'","")
        dataRaw = dataRaw.replace("\\n","")
        #Séparation des variables
        dataTab = dataRaw.split(";")
        data = {}
        """Amélioration : utiliser un dictionnaire?"""
        print(data)
        print(type(data))
        dataTab = data.split(";")
        
        
        valeurAccRaw = str(dataTab[0])
        valeurBattRaw = str(dataTab[1])
        print(valeurAccRaw)
        print(type(valeurAccRaw))
        
        #Traitement :
        
        ##Accélérateur
        valeurAcc = int(int(valeurAccRaw)/1023*100)
        accelerateurValeur.set(valeurAcc)
        valeurAccStr.set(str(valeurAcc) + " %")
        
        ##Batterie
        valeurBatt = int(int(valeurBattRaw)/1023*100)
        batterieValeur.set(valeurBatt)
        valeurBattStr.set(str(valeurBatt) + " %")
        
        #Mise à jour affichage
        fenetre.update()

fenetre = Tk()
fenetre.title("Dashboard")

accelerateurValeur = IntVar()
valeurAccStr = StringVar()
valeurAccStr.set("N/A")

batterieValeur = IntVar()
valeurBattStr = StringVar()
valeurBattStr.set("N/A")

cadre = ttk.Frame(fenetre, padding="3 3 12 12")
cadre.grid(column=0, row=0, sticky=(N, W, E, S))
cadre.columnconfigure(0, weight=1)
cadre.rowconfigure(0, weight=1)

#Cadre Accélérateur
frameAcc = ttk.Labelframe(cadre, text='Accélérateur', padding="3 3 12 12")
frameAcc.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Progressbar(frameAcc, orient=HORIZONTAL, length=400, mode='determinate', variable=accelerateurValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
ttk.Label(frameAcc, textvariable=valeurAccStr).grid(column=1, row=2)

#Cadre Batterie
frameBatt = ttk.Labelframe(cadre, text='Batterie', padding="3 3 12 12")
frameBatt.grid(column=1, row=0, sticky=(N, W, E, S))

ttk.Progressbar(frameBatt, orient=VERTICAL, length=100, mode='determinate', variable=batterieValeur, maximum=100).grid(column=1, row=1, sticky=(W, E))
ttk.Label(frameBatt, textvariable=valeurBattStr).grid(column=1, row=2)

ttk.Button(cadre, text="start", command=getData).grid(column=0, row=1)
ttk.Button(cadre, text="quitter", command=fenetre.destroy).grid(column=1, row=1)

fenetre.mainloop()

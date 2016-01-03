#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  setupSecurite.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  

from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import hashlib

from fonctionsSecurite import *

def setupSecurite():
    
    def select(chiffre,pinVars,SpinVars):
        i = 0
        while(i < 4):
            if pinVars[i].get() == -1:
                pinVars[i].set(chiffre)
                SpinVars[i].set(str(chiffre))
                if i == 3:
                    #Saisie terminée!
                    pin = str(pinVars[0].get()*1000+pinVars[1].get()*100+pinVars[2].get()*10+pinVars[3].get())
                    if messagebox.askyesno("Confirmation", "Souhaitez vous utiliser " + pin + " comme PIN?", icon="warning"):
                        #Calcul du hash
                        hashPin = hashlib.sha256(pin.encode('utf-8')).hexdigest()
                        #Génération du token
                        token = genToken()
                        hashToken = hashlib.sha256(token.encode('utf-8')).hexdigest()
                        #Ecriture
                        ecrireSecure(hashPin,hashToken)
                        #Montrer page d'explication pour installer le token
                        texte = "Le programme de démarrage a généré un token permettant une identification à deux facteurs.\n"
                        texte += "\nVeuillez placer le fichier \"OpenHyBike.token\" à la racine d'une clé usb et configurer /etc/fstab pour qu'elle soit montée dans le dossier \"conf/token\" lorsqu'elle est inserée.\n"
                        texte += "\nNe perdez surtout pas cette clé, sans elle il sera impossible de démarrer !"
                        messagebox.showinfo("Information",texte)
                        #Kill la fenetre / tuer programme?
                        quit()
                    else:
                        #On recommence
                        for pin in pinVars:
                            pin.set(-1)
                        for Spin in SpinVars:
                            Spin.set("_")
                        break
                else:
                    break
            else:
                i += 1
    
    def ecrireSecure(hashPIN,hashToken):
        secure = open("conf/secure","w")
        secure.write(hashPIN+"\n")
        secure.write(hashToken+"\n")
        secure.close()
        
    """Interface"""
    fenetre = Tk()
    fenetre.title("Démarrage")
    #fenetre.geometry("800x480")
    
    """Variables"""
    pin0 = IntVar() 
    pin1 = IntVar()
    pin2 = IntVar()
    pin3 = IntVar()
    Spin0 = StringVar() 
    Spin1 = StringVar()
    Spin2 = StringVar()
    Spin3 = StringVar()
    
    pinVars = [pin0,pin1,pin2,pin3]
    SpinVars = [Spin0,Spin1,Spin2,Spin3]
    
    for pin in pinVars:
        pin.set(-1)
        
    for Spin in SpinVars:
        Spin.set("_")    
    
    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=1, row=1, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)
    
    ttk.Label(cadre, text="Veuillez saisir un nouveau PIN :").grid(column=1, row=1, columnspan=4)
    
    cadrePin = ttk.Frame(cadre, padding="5 5 5 5")
    cadrePin.grid(column=1, row=2, sticky=(N, W, E, S), columnspan=4)
    
    ttk.Label(cadrePin, text=" ").grid(column=0, row=1, padx=28, sticky=(N, W, E, S))
    ttk.Label(cadrePin, textvariable=Spin0).grid(column=1, row=1, padx=5, pady=5, sticky=(N, W, E, S))
    ttk.Label(cadrePin, textvariable=Spin1).grid(column=2, row=1, padx=5, pady=5, sticky=(N, W, E, S))
    ttk.Label(cadrePin, textvariable=Spin2).grid(column=3, row=1, padx=5, pady=5, sticky=(N, W, E, S))
    ttk.Label(cadrePin, textvariable=Spin3).grid(column=4, row=1, padx=5, pady=5, sticky=(N, W, E, S))

    
    cadreBoutons = ttk.Frame(cadre, padding="5 5 5 5")
    cadreBoutons.grid(column=1, row=3, sticky=(N, W, E, S), columnspan=4)
    
    Button(cadreBoutons, text="7", command=lambda:select(7,pinVars,SpinVars), width=5, height=4).grid(column=1, row=1)
    Button(cadreBoutons, text="8", command=lambda:select(8,pinVars,SpinVars), width=5, height=4).grid(column=2, row=1)
    Button(cadreBoutons, text="9", command=lambda:select(9,pinVars,SpinVars), width=5, height=4).grid(column=3, row=1)
    Button(cadreBoutons, text="4", command=lambda:select(4,pinVars,SpinVars), width=5, height=4).grid(column=1, row=2)
    Button(cadreBoutons, text="5", command=lambda:select(5,pinVars,SpinVars), width=5, height=4).grid(column=2, row=2)
    Button(cadreBoutons, text="6", command=lambda:select(6,pinVars,SpinVars), width=5, height=4).grid(column=3, row=2)
    Button(cadreBoutons, text="1", command=lambda:select(1,pinVars,SpinVars), width=5, height=4).grid(column=1, row=3)
    Button(cadreBoutons, text="2", command=lambda:select(2,pinVars,SpinVars), width=5, height=4).grid(column=2, row=3)
    Button(cadreBoutons, text="3", command=lambda:select(3,pinVars,SpinVars), width=5, height=4).grid(column=3, row=3)
    Button(cadreBoutons, text="0", command=lambda:select(0,pinVars,SpinVars), width=5, height=4).grid(column=2, row=4)
    
    
    fenetre.mainloop()
    return 0

if __name__ == '__main__':
    
    setupSecurite()

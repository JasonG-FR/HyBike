#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  interfaceSecurite.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#  

from tkinter import *
from tkinter import ttk
import hashlib
from tkinter import messagebox



def interfaceSecurite():
    
    accesAutorise = [False]
    
    def getToken():
        #prendre en compte la valeur du fichier sur la clé et l'UUID (La clé doit être enregistée dans fstab et montée automatiquement)
        #hash-sha256: contenuFichier
        try:
            token = open("conf/token/OpenHyBike.token","r")
            Token = token.readline()
            token.close()
            return Token

        except FileNotFoundError:
            #"Clé non trouvée (fstab à jour?)
            messagebox.showwarning("Erreur", "Clé d'antivol numérique non détectée !")
            return "0"
        
    def validation(pin,hashPin):
        hashTest = hashlib.sha256(pin.encode('utf-8')).hexdigest()
        return hashTest == hashPin

    def select(chiffre,pinVars,SpinVars,accesAutorise):
        i = 0
        while(i < 4):
            if pinVars[i].get() == -1:
                pinVars[i].set(chiffre)
                SpinVars[i].set("*")
                if i == 3:
                    fichier = open("conf/secure","r")
                    hashPin = fichier.readline().replace("\n","")
                    hashToken = fichier.readline().replace("\n","")
                    fichier.close()
                    
                    pinTest = str(pinVars[0].get()*1000+pinVars[1].get()*100+pinVars[2].get()*10+pinVars[3].get())
                    tokenTest = getToken()
                    
                    if validation(pinTest,hashPin) and validation(tokenTest,hashToken):
                        #On valide l'accès
                        accesAutorise[0] = True
                        fenetre.destroy()
                    else:
                        #Recommencer la saisie!
                        messagebox.showwarning("Erreur", "Mauvaise clé d'antivol numérique et/ou mauvais mot de passe !")
                        for pin in pinVars:
                            pin.set(-1)
                        for Spin in SpinVars:
                            Spin.set(" ")
                        break
                    
                else:
                    break
            else:
                i += 1
        
                
    """Interface"""
    fenetre = Tk()
    fenetre.title("OpenHyBike")
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
        Spin.set(" ")    
    
    """Widgets"""
    cadre = ttk.Frame(fenetre, padding="5 5 5 5")
    cadre.grid(column=1, row=1, sticky=(N, W, E, S))
    cadre.columnconfigure(0, weight=1)
    cadre.rowconfigure(0, weight=1)
    
    ttk.Label(cadre, text="OpenHyBike").grid(column=1, row=1, columnspan=4)
    
    cadrePin = ttk.Frame(cadre, padding="5 5 5 5")
    cadrePin.grid(column=1, row=2, sticky=(N, W, E, S))
    
    ttk.Label(cadrePin, text="PIN ?").grid(column=1, row=1, padx=86, columnspan=4, pady=10)
    ttk.Label(cadrePin, textvariable=Spin0).grid(column=1, row=2, padx=5, pady=5)
    ttk.Label(cadrePin, textvariable=Spin1).grid(column=2, row=2, padx=5, pady=5)
    ttk.Label(cadrePin, textvariable=Spin2).grid(column=3, row=2, padx=5, pady=5)
    ttk.Label(cadrePin, textvariable=Spin3).grid(column=4, row=2, padx=5, pady=5)

    
    cadreBoutons = ttk.Frame(cadre, padding="5 5 5 5")
    cadreBoutons.grid(column=1, row=3, sticky=(N, W, E, S), columnspan=4)
    
    Button(cadreBoutons, text="7", command=lambda:select(7,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=1, row=1)
    Button(cadreBoutons, text="8", command=lambda:select(8,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=2, row=1)
    Button(cadreBoutons, text="9", command=lambda:select(9,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=3, row=1)
    Button(cadreBoutons, text="4", command=lambda:select(4,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=1, row=2)
    Button(cadreBoutons, text="5", command=lambda:select(5,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=2, row=2)
    Button(cadreBoutons, text="6", command=lambda:select(6,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=3, row=2)
    Button(cadreBoutons, text="1", command=lambda:select(1,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=1, row=3)
    Button(cadreBoutons, text="2", command=lambda:select(2,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=2, row=3)
    Button(cadreBoutons, text="3", command=lambda:select(3,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=3, row=3)
    Button(cadreBoutons, text="0", command=lambda:select(0,pinVars,SpinVars,accesAutorise), width=5, height=4).grid(column=2, row=4)
    
    
    fenetre.mainloop()
    
    return accesAutorise[0]

if __name__ == '__main__':
    
    print(interfaceSecurite())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  updateData.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#  
#

from tkinter import *
from time import sleep

from fonctionsArduino import *
from fonctionsData import *
from moyennes import *
from fonctionsLogs import *
from formatH import *

def updateData(tkVars, tkObj, moyennes, params, dataTab, data, fichier=False, tpsConsigne=0, tempo=1, donnees=0):
    #   Permet de mettre à jour les variables d'affichage de l'interface avec les données Arduino
    # 
    #   @param : 
    #       tkVars : dictionnaire contenant toutes les variables de l'affichage
    #       tkObj : dictionnaire contenant tous les objets à modifier
    #       moyennes : dictionnaire qui contient toutes les séries de données utilisées pour le calcul des moyennes
    #       params : dictionnaire contenant les valeurs des paramètres
    #       dataTab : liste contenant les valeurs de l'arduino (issue de decodageArduino)
    #       data : dictionnaire contenant les valeurs convertie et classées
    #       (fichier) : objet contenant le fichier de log à écrire
    #       (tempsConsigne) : variable stockant la valeur du temps limite de la tempo pour les logs
    #       (tempo) : temporisation pour enregistrer les données dans le log (en seconde)
    #       (donnees) : liste des valeurs à écrire dans le log
    #
    #
    
    
    #Vérifier si le flux est complet, sinon attendre qu'il n'y ait plus d'erreurs
    try:
        """Conversion des données Arduino"""
        convArduino(dataTab, data)

        """Mise à jour des variables de l'interface"""
        conso = moyennes["conso"]
        vite = moyennes["vite"]
        
        ##Accélérateur
        majProgressBar(data["valAcc"],tkVars["accelerateurValeur"],tkVars["valeurAccStr"])

        ##Frein
        majProgressBar(data["valFrein"],tkVars["freinValeur"],tkVars["valeurFreinStr"])
    
        ##Batterie
        majProgressBar(data["valBatt"],tkVars["batterieValeur"],tkVars["valeurBattStr"])
        Tension = data["valBatt"]*(params["maxVBat"]-params["minVBat"])/100.+params["minVBat"]
        tkVars["voltageBattStr"].set("{0:.2f}".format(Tension) + " V")
            
        majCouleur(data["valBatt"],tkObj["lbatt"],"green",30,"orange",10,"red")
            
        """Le choix de cet algorithme de calcul est à vérifier (cycle de décharge non linéaire, estimation energie à calibrer) -> cf fichier ODC"""
        energie = params["capBat"]*params["maxVBat"]*data["valBatt"]/100
        tkVars["energieBattStr"].set("{0:.2f}".format(energie) + " Wh")
    
        ##Consommation
        Intensite = convBinNumCentre(params["I0"],data["valIntensite"],params["Imax"])
        puissance = Tension*Intensite
                
        if puissance > 0:
            #Décharge
            majProgressBar(puissance,tkVars["puissanceValeurConso"],tkVars["valeurPuisConsoStr"],0,"W")
            majProgressBar(0,tkVars["puissanceValeurProd"],tkVars["valeurPuisProdStr"],0,"W")
                
        elif puissance < 0:
            #Charge
            majProgressBar(0,tkVars["puissanceValeurConso"],tkVars["valeurPuisConsoStr"],0,"W")
            majProgressBar(-1*puissance,tkVars["puissanceValeurProd"],tkVars["valeurPuisProdStr"],0,"W")
                
        else:
            #Arrêt
            majProgressBar(0,tkVars["puissanceValeurConso"],tkVars["valeurPuisConsoStr"],0,"W")
            majProgressBar(0,tkVars["puissanceValeurProd"],tkVars["valeurPuisProdStr"],0,"W")
            
        moyenneDynamique(conso,puissance,params["majMoy"])
        tkVars["moyenneConso"].set("{0:.0f}".format(conso["moy"]) + " W")
        majCouleur(conso["moy"],tkObj["lMoyConso"],"red",0,"green")
            
        if conso["moy"] > 0:
            autonomie = energie/conso["moy"]
            tkVars["estimationBatt"].set("~ " + formatH(autonomie))
        else:
            autonomie = -1
            tkVars["estimationBatt"].set("N/A")
        
        ##Vitesse
        vitesse = data["valVitesse"]*params["Vmax"]/100
            
        majProgressBar(vitesse,tkVars["vitesseValeur"],tkVars["valeurVitesseStr"],0,"km/h   <=>   "+"{0:.1f}".format(vitesse*10/36.) + " m/s")
            
        moyenneDynamique(vite,vitesse,params["majMoy"])
        tkVars["moyenneVitesse"].set("Vitesse moyenne : " + "{0:.1f}".format(vite["moy"]) + " km/h")
            
        if autonomie < 0:
            tkVars["estimationVitesse"].set("Autonomie restante : N/A")
        else:
            tkVars["estimationVitesse"].set("Autonomie restante : ~ " + "{0:.0f}".format(vite["moy"]*autonomie) + " km")
            
        ##Mise à jour du log si actif
        if fichier != False:
            #[tps,acc,frein,ubat,imot,vit]
            donnees[1] = str(tkVars["accelerateurValeur"].get())
            donnees[2] = str(tkVars["freinValeur"].get())
            donnees[3] = "{0:.2f}".format(Tension)
            donnees[4] = "{0:.2f}".format(Intensite)
            donnees[5] = "{0:.1f}".format(tkVars["vitesseValeur"].get())
            logSession(fichier,donnees,tpsConsigne,tempo)
            
    except ValueError:
        #Pause de 10ms
        sleep(0.01)
    except IndexError:
        #Pause de 10ms
        sleep(0.01)

if __name__ == '__main__':
    exit()

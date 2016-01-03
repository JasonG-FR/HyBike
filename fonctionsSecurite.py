#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  fonctionsSecurite.py
#  
#  Copyright 2016 Jason Gombert <jason.gombert@gmail.com>
#    
#  

import random


def genToken():
    
    token = open("OpenHyBike.token","w")
    chars = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
    strToken = ""
    for i in range(4096):
        strToken += random.choice(chars)
    token.write(strToken)
    token.close()

if __name__ == '__main__':
    
    genToken()

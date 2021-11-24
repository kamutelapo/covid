#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

FILE=sys.argv[1]


def tablaKinyeres(content):
    sor = 0
    maxSor = len(content)

    while(sor < maxSor and len(content[sor]) == 0):
        sor += 1
    
    lista = []
    while sor < maxSor:
        
        ndx=0
        while sor < maxSor and len(content[sor]) != 0:
            if ndx >= len(lista):
                lista.append([])
            lista[ndx].append(content[sor])
            sor += 1
            ndx += 1
        
        sor += 1

    for rw in lista:
        print ("\"" + ("\",\"".join(rw)) + "\"")
    quit()
    

text_file = open(FILE, "r")
lines = text_file.readlines()
text_file.close()
    
lines = list(map(lambda x:x.strip(),lines))

tablaKinyeres(lines)

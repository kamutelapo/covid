#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

FILE=sys.argv[1]


def tablaKinyeres(content):
    sor = 0
    maxSor = len(content)

    while(len(content[sor]) == 0):
        sor += 1
    
    lista = []
    while sor < maxSor:
        cella = content[sor]
        sor = sor+1
        while sor < maxSor and len(content[sor]) != 0:
            cella += " " + content[sor]
            sor = sor+1
        
        lista.append(cella)
        sor = sor+1

    hdrndx = lista.index("=====")
    
    hdr = lista[0 : hdrndx]
    remaining = lista[hdrndx+1:]
    
    hdrl = len(hdr)
    composite_list = [remaining[x:x+hdrl] for x in range(0, len(remaining),hdrl)]
    
    hdrstr = "\"" + ("\",\"".join(hdr)) + "\""
    
    print (hdrstr)

    for l in composite_list:
        datastr = "\"" + ("\",\"".join(l)) + "\""
        print (datastr)
    

text_file = open(FILE, "r")
lines = text_file.readlines()
text_file.close()
    
lines = list(map(lambda x:x.strip(),lines))

tablaKinyeres(lines)

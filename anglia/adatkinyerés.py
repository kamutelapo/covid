#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

def processReport(hetszama, content):
    print ("TODO", hetszama)
    pass


FILEDIR=sys.argv[1]

SZAM_PATTERN = re.compile(r'^.*week\s*_?\-?\s*(\d+).*$')

for filename in os.listdir(FILEDIR):
  if filename.endswith(".txt"): 
    path = os.path.join(FILEDIR, filename)
    
    text_file = open(path, "r")
    lines = text_file.readlines()
    text_file.close()
    
    mtch = SZAM_PATTERN.match(filename)    
    if mtch:
      szam = int(mtch.group(1))
      processReport(szam, lines)
    else:
      print ("Programhiba", filename)
      quit()
    
print ("TODO: utofeldolgozas")


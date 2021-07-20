#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd

DATADIR=os.path.dirname(__file__) + "/adatok"

DATE_PATTERN = re.compile(r'^\s*#####\s+(.*)$')

LELEGEZTET = re.compile(r'.*[^\d](\d+)\s*-\s*.n\s+vannak\s+lélegeztetőgépen.*', re.S)

file1 = open(DATADIR +"/nyersadatok.txt", 'r', encoding='utf-8', errors='ignore')
lines = file1.readlines()
file1.close()

df = pd.DataFrame(columns=['Dátum','Lélegeztetettek'])


while (lines):
  line = lines.pop(0)
  
  mtch = DATE_PATTERN.match(line)
  
  if mtch:
    date = mtch.group(1)
    
    arr = []
    
    while (len(lines) > 0) and (not DATE_PATTERN.match(lines[0])):
        arr.append(lines.pop(0))
    
    body = ''.join(arr)
    
    lelegezteton = None
    
    mtch = LELEGEZTET.match(body)
    if mtch:
        lelegezteton = mtch.group(1)
    else:
        if "léleg" in body.lower():
            print (body)
            quit()

    ujsor = {
        "Dátum": date,
        "Lélegeztetettek": lelegezteton,
    }
    
    df = df.append(ujsor, ignore_index=True)


df.to_csv(DATADIR +"/hiradatok.csv", index = False)

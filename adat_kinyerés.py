#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import numpy as np
import datetime

DATADIR=os.path.dirname(__file__) + "/adatok"

DATE_PATTERN = re.compile(r'^\s*#####\s+(.*)$')

LELEGEZTET = re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s*-\s*.n\s+vannak\s+lélegeztetőgépen.*', re.S)


ELHUNYTAK_SZAMA = [
    re.compile(r'.*[eE]zzel\s+([0-9\s+]+)\s*-\s*r?[ae]\s+emelkedett\s+az\s+elhunytak\s+száma.*', re.S),
    re.compile(r'.*[eE]zzel\s+([0-9\s+]+)\s*főre\s+emelkedett\s+az\s+elhunytak\s+száma.*', re.S),
    re.compile(r'.*[aA]z\s+elhunytak\s+száma\s+([0-9\s+]+)\s*fő.*', re.S),
    re.compile(r'.*[aA]z\s+elhunytak\s+száma,?\s+változatlanul\s+([0-9\s+]+)\s*fő.*', re.S),
    re.compile(r'.*[aA]z\s+elhunytak\s+száma\s+így\s+([0-9\s+]+)\s*főre.*', re.S),
    re.compile(r'.*[aA]z\s+elhunytak\s+száma\s*,\s+immár\s+negyedik\s+napja\s+változatlanul\s+([0-9\s+]+)\s*fő.*', re.S),
    re.compile(r'.*így\s+([0-9\s+]+)\s*-\s*r?[ae]\s+emelkedett\s+az\s+elhunytak\s+száma.*', re.S),
    re.compile(r'.*így\s+változatlanul\s+([0-9\s+]+)\s*az\s+elhunytak\s+száma.*', re.S),
]

BEOLTOTTAK_SZAMA = [
    re.compile(r'.*[aA]\s+beoltott(?:ak)?\s+száma\s+([0-9\s+]+)\s*fő', re.S),
    re.compile(r'.*[aA]\s+beoltottak\s+száma\s+([0-9\s+]+)\s*,?\s*közülük', re.S),
    re.compile(r'.*[aA]\s+beoltottak\s+száma\s+([0-9\s+]+)\s*,?\s*közülük', re.S),
    re.compile(r'.*Több\s+mint\s+([0-9\s+]+)\s*a\s+beoltottak\s+száma.*', re.S),
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s*fő\s+a\s+beoltottak\s+száma.*', re.S),
    re.compile(r'.*[eE]ddig\s+([0-9\s+]+)\s*fő\s+kapott\s+oltást.*', re.S),
    re.compile(r'.*[mM]ár\s+([0-9\s+]+)\s*fő\s+kapott\s+oltást.*', re.S),
]

file1 = open(DATADIR +"/nyersadatok.txt", 'r', encoding='utf-8', errors='ignore')
lines = file1.readlines()
file1.close()

df = pd.DataFrame(columns=['Dátum', 'Elhunytak', 'Lélegeztetettek','Beoltottak'])


while (lines):
  line = lines.pop(0)
  
  mtch = DATE_PATTERN.match(line)
  
  if mtch:
    date = mtch.group(1)
    
    if date == '2020-04-07':
        break
    
    arr = []
    
    while (len(lines) > 0) and (not DATE_PATTERN.match(lines[0])):
        arr.append(lines.pop(0))
    
    body = ''.join(arr)
    
    lelegezteton = None
    elhunytak = None
    beoltottak = None
    
    mtch = LELEGEZTET.match(body)
    if mtch:
        lelegezteton = mtch.group(1)
        lelegezteton = re.sub(r'\s', '', lelegezteton)
    else:
        if "léleg" in body.lower():
            print (body)
            quit()

    for pattern in ELHUNYTAK_SZAMA:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        elhunytak = mtch.group(1)
        elhunytak = re.sub(r'\s', '', elhunytak)
    else:
        if "elhunytak" in body.lower():
            print (body)
            quit()

    for pattern in BEOLTOTTAK_SZAMA:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        beoltottak = mtch.group(1)
        beoltottak = re.sub(r'\s', '', beoltottak)
    else:
        if date == '2021-03-30':
            beoltottak = 2000998
        elif date == '2021-03-08':
            beoltottak = 1002714
        elif "oltott" in body.lower():
            print (body)
            quit()
    
    if elhunytak is None:
        continue

    ujsor = {
        "Dátum": datetime.datetime.strptime(date, '%Y-%m-%d'),
        "Elhunytak": elhunytak,
        "Lélegeztetettek": lelegezteton,
        "Beoltottak": beoltottak,
    }
    
    df = df.append(ujsor, ignore_index=True)


df[['Elhunytak']] = df[['Elhunytak']].astype(float)
df[['Lélegeztetettek']] = df[['Lélegeztetettek']].astype(float)
df[['Beoltottak']] = df[['Beoltottak']].astype(float)

mindate = df['Dátum'].min()
maxdate = df['Dátum'].max()

ddf = pd.DataFrame(pd.date_range(start = mindate, end = maxdate), columns=['Dátum'])
df = pd.merge(ddf, df, left_on = 'Dátum', right_on = 'Dátum', how="outer")

df['Elhunytak'] = (df['Elhunytak'].interpolate(method='linear') + 0.5).astype(int)
df['Beoltottak'] = (df['Beoltottak'].interpolate(method='linear') + 0.5).apply(np.floor)
df['Lélegeztetettek'] = df.apply(lambda row: None if np.isnan(row['Lélegeztetettek']) else str(int(row['Lélegeztetettek'])), axis = 1 )

elozoertek = df.iloc[:-1]['Elhunytak']
elsoelozo = pd.DataFrame([[47]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új elhunyt']
df['Napi új elhunyt'] = df['Elhunytak'] - elozoertek['Napi új elhunyt'] 

elozoertek = df.iloc[:-1]['Beoltottak']
elsoelozo = pd.DataFrame([[np.NaN]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új beoltott']
df['Napi új beoltott'] = df['Beoltottak'] - elozoertek['Napi új beoltott'] 

df['Beoltottak'] = df.apply(lambda row: None if np.isnan(row['Beoltottak']) else str(int(row['Beoltottak'])), axis = 1 )
df['Napi új beoltott'] = df.apply(lambda row: None if np.isnan(row['Napi új beoltott']) else str(int(row['Napi új beoltott'])), axis = 1 )

#pd.set_option("display.max_rows", None)
#print (df)

df.to_csv(DATADIR +"/hiradatok.csv", index = False)

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
    re.compile(r'.*[aA]z\s+elhunytak\s+száma\s+([0-9\s+]+)\s*emelkedett.*', re.S),
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

KETSZER_OLTOTTAK_SZAMA = [
    re.compile(r'.*közülük\s+([0-9\s+]+)\s*fő\s+már\s+a\s+második.*', re.S),
    re.compile(r'.*közülük\s+([0-9\s+]+)\s*már\s+a\s+második\s+oltását\s+is\s+megkapta.*', re.S),
    re.compile(r'.*ebből\s+([0-9\s+]+)\s*fő\s+már\s+a\s+második\s+oltását\s+is\s+megkapta.*', re.S),
    re.compile(r'.*,\s*([0-9\s+]+)\s*fő\s+már\s+a\s+második\s+oltását\s+is\s+megkapta.*', re.S),
]

HAROMSZOR_OLTOTTAK_SZAMA = [
    re.compile(r'.*[^0-9]([0-9\s+]\s*millió\s+[0-9\s+]+)\s*ezren\s+(?:pedig)?\s*már\s+a\s+harmadik\s+oltást\s+is\s+felvették.*', re.S),
    re.compile(r'.*[^0-9]([0-9\s+]+\s*ezren)\s+(?:pedig)?\s*már\s+a\s+harmadik\s+oltást\s+is\s+felvették.*', re.S),
    re.compile(r'.*Már\s+([0-9\s+]+\s*ezren)\s+a\s+harmadik\s+oltást\s+is\s+felvették.*', re.S),
    re.compile(r'.*harmadik\s+oltásra\s+és\s+([0-9\s+]+\s*ezren)\s+már\s+fel\s+is\s+vették\s+azt.*', re.S),
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s+(?:fő\s+)?pedig\s+már\s+a\s+harmadik\s+oltást\s+is\s+felvették.*', re.S),
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s+(?:fő\s+)?pedig\s+már\s+a\s+megerősítő\s+harmadik\s+oltását\s+is\s+felvette.*', re.S),
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s+fő\s+már\s+harmadik\s+oltását\s+is\s+felvette.*', re.S),
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s+fő\s+harmadik,.*', re.S),
]

NEGYSZER_OLTOTTAK_SZAMA = [
    re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s+fő\s+már\s+a\s+negyedik\s+oltását\s+is\s+felvette.*', re.S),
]

KORHAZBAN = [
    [False, re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s*koronavírusos\s+beteget\s+ápolnak\s+kórházban.*', re.S)],
    [True,  re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s*beteget\s+ápolnak\s+kórházban\s+lélegeztetés\s+nélkül.*', re.S)],
    [False, re.compile(r'.*[^0-9\s+]([0-9\s+]+)\s*fő\s+igényel\s+kórházi\s+kezelést.*', re.S)],
    [False, re.compile(r'.*\(([0-9\s+]+)\s*fő\s*\)\s*kórházi\s+ellátásra\s+szorul.*', re.S)],
]

OSSZES_FERTOZOTT = [
    re.compile(r'.*összesen\s+([0-9][0-9\s+]*)\s*főre\s+nőtt\s+a\s+beazonosított\s+fertőzöttek\s+száma.*', re.S),
    re.compile(r'.*ezzel\s+([0-9][0-9\s+]*)\s*főre\s+nőtt\s+a\s+hazánkban\s+beazonosított\s+fertőzöttek\s+száma.*', re.S),
    re.compile(r'.*ezzel\s+([0-9][0-9\.]*)\s*főre\s+nőtt\s+a\s+hazánkban\s+beazonosított\s+fertőzöttek\s+száma.*', re.S),
    re.compile(r'.*összesen\s+([0-9][0-9\s+]*)\s*nőtt\s+a\s+beazonosított\s+fertőzöttek\s+száma.*', re.S),
]

file1 = open(DATADIR +"/nyersadatok.txt", 'r', encoding='utf-8', errors='ignore')
lines = file1.readlines()
file1.close()

df = pd.DataFrame(columns=['Dátum', 'Elhunytak', 'Lélegeztetettek','Beoltottak', 'Kétszer oltottak', 'Kórházban ápoltak', 'Összes fertőzött'])

processed_dates = set()

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
    
    if ("Törökországban" in body) and ("Oroszországban" in body) and ("Spanyolországban" in body):
        continue
    
    lelegezteton = None
    elhunytak = None
    beoltottak = None
    ketszeroltottak = None
    haromszoroltottak = None
    negyszeroltottak = None
    korhazban = None
    osszesfertozott = None
    
    mtch = LELEGEZTET.match(body)
    if mtch:
        lelegezteton = mtch.group(1)
        lelegezteton = re.sub(r'\s', '', lelegezteton)
    else:
        if "léleg" in body.lower():
            print (body)
            print ("a lélegeztetetteknél gond van")
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
            print ("az elhunytaknál gond van")
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
        elif date == '2021-12-27':
            # nincs adat
            pass
        elif "oltott" in body.lower():
            print (body)
            print ("az oltottaknál gond van")
            quit()


    for pattern in KETSZER_OLTOTTAK_SZAMA:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        ketszeroltottak = mtch.group(1)
        ketszeroltottak = re.sub(r'\s', '', ketszeroltottak)
    else:
        if date == '2021-03-30':
            # nincs adat
            pass
        elif date == '2021-03-08':
            # nincs adat
            pass
        elif date == '2021-12-27':
            # nincs adat
            pass
        elif "második olt" in body.lower() or "kétszer olt" in body.lower():
            print (body)
            print ("a másodszor oltottaknál gond van")
            quit()


    for pattern in HAROMSZOR_OLTOTTAK_SZAMA:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        haromszoroltottak = mtch.group(1)
        haromszoroltottak = re.sub(r'\s', '', haromszoroltottak)

        if "millió" in haromszoroltottak:
            arr = haromszoroltottak.split("millió")
            haromszoroltottak = int(arr[0])*1000000 + int(arr[1]) * 1000
        elif "ezren" in haromszoroltottak:
            haromszoroltottak = re.sub(r'ezren', '', haromszoroltottak)
            haromszoroltottak = int(haromszoroltottak)*1000
        else:
            haromszoroltottak = str(int(haromszoroltottak))
    else:
        if (date > '2021-08-03') and ("háromszor oltott" in body.lower() or "harmadik oltás" in body.lower()):
            if date != '2021-08-11':
              print (body)
              print ("a háromszor oltottaknál gond van")
              quit()
        if date <= '2021-08-03':
            haromszoroltottak = "0"

    for pattern in NEGYSZER_OLTOTTAK_SZAMA:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        negyszeroltottak = mtch.group(1)
        negyszeroltottak = re.sub(r'\s', '', negyszeroltottak)

        negyszeroltottak = str(int(negyszeroltottak))
    else:
        if (date > '2022-02-13') and ("négyszer oltott" in body.lower() or "negyedik oltás" in body.lower()):
            if not ((date >= '2022-02-15') and (date <= '2023-02-18')):
                print (body)
                print ("a négyszer oltottaknál gond van")
                quit()
        if date <= '2022-02-13':
            negyszeroltottak = "0"

    lelegeztetettek_nelkul = False
    for pattern in KORHAZBAN:
        lelegeztetettek_nelkul = pattern[0]
        mtch = pattern[1].match(body)
        if mtch:
            break

    if mtch:
        korhazban = mtch.group(1)
        korhazban = re.sub(r'\s', '', korhazban)

        if lelegeztetettek_nelkul:
            korhazban = str(int(korhazban) + int(lelegezteton))
    else:
        if "kórház" in body.lower() and "ápol" in body.lower():
            print (body)
            print ("a kórházi kezeléseknél gond van")
            quit()

    for pattern in OSSZES_FERTOZOTT:
        mtch = pattern.match(body)
        if mtch:
            break

    if mtch:
        osszesfertozott = mtch.group(1)
        osszesfertozott = re.sub(r'\s', '', osszesfertozott)
        osszesfertozott = re.sub(r'\.', '', osszesfertozott)
    else:
        if "összes fertőz" in body.lower():
            print (body)
            print ("az összes fertőzöttnél gond van")
            quit()

    if elhunytak is None:
        continue
    
    if date in processed_dates:
        print (body)
        print ("Dupla")
        quit()
    processed_dates.add(date)
    
    ujsor = {
        "Dátum": datetime.datetime.strptime(date, '%Y-%m-%d'),
        "Elhunytak": elhunytak,
        "Lélegeztetettek": lelegezteton,
        "Beoltottak": beoltottak,
        "Kétszer oltottak": ketszeroltottak,
        "Háromszor oltottak": haromszoroltottak,
        "Négyszer oltottak": negyszeroltottak,
        "Kórházban ápoltak": korhazban,
        "Összes fertőzött": osszesfertozott,
    }
    
    df = df.append(ujsor, ignore_index=True)


df[['Elhunytak']] = df[['Elhunytak']].astype(float)
df[['Lélegeztetettek']] = df[['Lélegeztetettek']].astype(float)
df[['Beoltottak']] = df[['Beoltottak']].astype(float)
df[['Kétszer oltottak']] = df[['Kétszer oltottak']].astype(float)
df[['Háromszor oltottak']] = df[['Háromszor oltottak']].astype(float)
df[['Négyszer oltottak']] = df[['Négyszer oltottak']].astype(float)
df[['Összes fertőzött']] = df[['Összes fertőzött']].astype(float)

mindate = df['Dátum'].min()
maxdate = df['Dátum'].max()

ddf = pd.DataFrame(pd.date_range(start = mindate, end = maxdate), columns=['Dátum'])
df = pd.merge(ddf, df, left_on = 'Dátum', right_on = 'Dátum', how="outer")

df['Elhunytak'] = (df['Elhunytak'].interpolate(method='linear') + 0.5).astype(int)
df['Beoltottak'] = (df['Beoltottak'].interpolate(method='linear') + 0.5).apply(np.floor)
df['Összes fertőzött'] = (df['Összes fertőzött'].interpolate(method='linear') + 0.5).apply(np.floor)
df['Kétszer oltottak'] = (df['Kétszer oltottak'].interpolate(method='linear') + 0.5).apply(np.floor)
df['Háromszor oltottak'] = (df['Háromszor oltottak'].interpolate(method='linear') + 0.5).apply(np.floor)
df['Négyszer oltottak'] = (df['Négyszer oltottak'].interpolate(method='linear') + 0.5).apply(np.floor)
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

elozoertek = df.iloc[:-1]['Kétszer oltottak']
elsoelozo = pd.DataFrame([[np.NaN]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új másodszor oltott']
df['Napi új másodszor oltott'] = df['Kétszer oltottak'] - elozoertek['Napi új másodszor oltott'] 

elozoertek = df.iloc[:-1]['Háromszor oltottak']
elsoelozo = pd.DataFrame([[np.NaN]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új harmadszor oltott']
df['Napi új harmadszor oltott'] = df['Háromszor oltottak'] - elozoertek['Napi új harmadszor oltott'] 

elozoertek = df.iloc[:-1]['Négyszer oltottak']
elsoelozo = pd.DataFrame([[np.NaN]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új negyedszer oltott']
df['Napi új negyedszer oltott'] = df['Négyszer oltottak'] - elozoertek['Napi új negyedszer oltott'] 

elozoertek = df.iloc[:-1]['Összes fertőzött']
elsoelozo = pd.DataFrame([[817]]);
elozoertek = pd.concat([elsoelozo, elozoertek], ignore_index=True)
elozoertek.columns = ['Napi új fertőzött']
df['Napi új fertőzött'] = df['Összes fertőzött'] - elozoertek['Napi új fertőzött'] 

df['Beoltottak'] = df.apply(lambda row: None if np.isnan(row['Beoltottak']) else str(int(row['Beoltottak'])), axis = 1 )
df['Kétszer oltottak'] = df.apply(lambda row: None if np.isnan(row['Kétszer oltottak']) else str(int(row['Kétszer oltottak'])), axis = 1 )
df['Háromszor oltottak'] = df.apply(lambda row: None if np.isnan(row['Háromszor oltottak']) else str(int(row['Háromszor oltottak'])), axis = 1 )
df['Napi új beoltott'] = df.apply(lambda row: None if np.isnan(row['Napi új beoltott']) else str(int(row['Napi új beoltott'])), axis = 1 )
df['Napi új másodszor oltott'] = df.apply(lambda row: None if np.isnan(row['Napi új másodszor oltott']) else str(int(row['Napi új másodszor oltott'])), axis = 1 )
df['Napi új harmadszor oltott'] = df.apply(lambda row: None if np.isnan(row['Napi új harmadszor oltott']) else str(int(row['Napi új harmadszor oltott'])), axis = 1 )
df['Napi új negyedszer oltott'] = df.apply(lambda row: None if np.isnan(row['Napi új negyedszer oltott']) else str(int(row['Napi új negyedszer oltott'])), axis = 1 )
df['Összes fertőzött'] = df.apply(lambda row: None if np.isnan(row['Összes fertőzött']) else str(int(row['Összes fertőzött'])), axis = 1 )
df['Napi új fertőzött'] = df.apply(lambda row: None if np.isnan(row['Napi új fertőzött']) else str(int(row['Napi új fertőzött'])), axis = 1 )

#pd.set_option("display.max_rows", None)
#print (df)

df.to_csv(DATADIR +"/hiradatok.csv", index = False)

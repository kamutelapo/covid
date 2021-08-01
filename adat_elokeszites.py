#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import datetime

osszeg_oszlopok = ["Aktív fertőzött", "Elhunyt", "Gyógyult", "Összesen", "Beoltottak"]
pillanat_oszlopok = ["Aktív fertőzöttek változása", "Napi új elhunyt", "Napi új gyógyult", "Napi új fertőzött", "Napi új beoltott"]
adat_oszlopok = osszeg_oszlopok + pillanat_oszlopok
minden_oszlop = ["Dátum"] + adat_oszlopok

DATADIR=os.path.dirname(__file__) + "/adatok"

csv1 = pd.read_csv(DATADIR +"/covidadatok1.csv", )
csv2 = pd.read_csv(DATADIR +"/covidadatok2.csv")
csv1[['Napi új fertőzött']] = csv1[['Napi új fertőzött']].astype(str)
csv1[['Aktív fertőzött']] = csv1[['Aktív fertőzött']].astype(str)

csvconcat = pd.concat([csv1, csv2], sort=True)
csvconcat = csvconcat.replace(np.nan, '0', regex=True)
csvout = csvconcat[minden_oszlop]

csvout['Aktív fertőzött'] = csvout['Aktív fertőzött'].str.replace(' ', '')
csvout['Aktív fertőzött'] = csvout['Aktív fertőzött'].str.replace(u'\u00a0', '')
csvout['Elhunyt'] = csvout['Elhunyt'].str.replace(' ', '')
csvout['Gyógyult'] = csvout['Gyógyult'].str.replace(' ', '')
csvout['Összesen'] = csvout['Összesen'].str.replace(' ', '')
csvout['Összesen'] = csvout['Összesen'].str.replace(u'\u00a0', '')
csvout['Beoltottak'] = csvout['Beoltottak'].str.replace(' ', '')
csvout['Napi új beoltott'] = csvout['Napi új beoltott'].str.replace(' ', '')
csvout['Napi új fertőzött'] = csvout['Napi új fertőzött'].str.replace(' ', '')

csvout[adat_oszlopok] = csvout[adat_oszlopok].apply(pd.to_numeric)
csvout=csvout.reset_index()

ujdf = pd.DataFrame(columns=minden_oszlop)
utolsoDatum = None
utolsoIndex = None

# interpoláció
for index, row in csvout.iterrows():
    datum = row["Dátum"]
    
    if utolsoDatum is not None:
        d2 = datetime.datetime.strptime(datum, '%Y.%m.%d')
        d1 = datetime.datetime.strptime(utolsoDatum, '%Y.%m.%d')
        
        kulonbseg = (d2 - d1).days
        if kulonbseg > 1:
            d1 = d1 + datetime.timedelta(days=1)
            
            jelenlegi = csvout.loc[index]
            utolso = csvout.loc[utolsoIndex]
            
            delta_osszeg = ((jelenlegi[osszeg_oszlopok] - utolso[osszeg_oszlopok]) / 3).apply(int)
            delta_pillanat = (jelenlegi[pillanat_oszlopok]/3).apply(int)
            maradek=jelenlegi[pillanat_oszlopok]
            
            interpolalt_osszeg = utolso[osszeg_oszlopok]
            
            while( d2 > d1 ):
                interpolalt_osszeg = interpolalt_osszeg + delta_osszeg
                maradek = maradek - delta_pillanat
                ujsor_osszeg = dict(zip(osszeg_oszlopok, interpolalt_osszeg))
                ujsor_pillanat = dict(zip(pillanat_oszlopok, delta_pillanat))
                ujsor = {**ujsor_osszeg,**ujsor_pillanat}
                ujsor["Dátum"] = d1.strftime('%Y.%m.%d')
                
                ujdf = ujdf.append(ujsor, ignore_index=True)
                
                d1 = d1 + datetime.timedelta(days=1)
            
            ujsor_osszeg = dict(zip(osszeg_oszlopok, jelenlegi[osszeg_oszlopok]))
            ujsor_pillanat = dict(zip(pillanat_oszlopok, maradek))
            ujsor = {**ujsor_osszeg,**ujsor_pillanat}
            ujsor["Dátum"] = d2.strftime('%Y.%m.%d')
            ujdf = ujdf.append(ujsor, ignore_index=True)
        else:
            ujdf = ujdf.append(row, ignore_index=True)
    else:
        ujdf = ujdf.append(row, ignore_index=True)
    
    utolsoDatum = datum
    utolsoIndex = index

del ujdf['index']
csvout = ujdf

csvout.to_csv(DATADIR +"/covidadatok.csv", index = False)

csv = pd.read_csv(DATADIR +"/covidadatok.csv", parse_dates=['Dátum'])
csv2 = pd.read_csv(DATADIR +"/hiradatok.csv", parse_dates=['Dátum'])

csvpart = csv[["Dátum", "Elhunyt"]]
csv2part = csv2[["Dátum", "Elhunytak"]]

csvpart = pd.merge(csvpart, csv2part, left_on = 'Dátum', right_on = 'Dátum', how="outer")
csvpart['Elhunyt'] = csvpart.apply(lambda row: row['Elhunytak'] if np.isnan(row['Elhunyt']) else row['Elhunyt'], axis = 1 )
csvpart[['Elhunyt']] = csvpart[['Elhunyt']].astype(int)

elhunytnap = []
last = 0

for index, row in csvpart.iterrows():
    datum = row['Dátum']
    elhunyt = row['Elhunyt']
    
    for i in range(last,elhunyt):
        elhunytnap.insert(0, datum)

    last = elhunyt


elhunytak = pd.read_csv(DATADIR +"/elhunytak.csv")

maxlen=(elhunytak.shape[0])

for i in range(last, maxlen):
    elhunytnap.insert(0, datum)

elhunytak['Dátum'] = elhunytnap

elhunytak[["Sorszám","Dátum","Nem","Kor","Alapbetegségek"]].to_csv(DATADIR +"/elhunytak_datummal.csv", index = False)

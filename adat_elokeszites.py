#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

adat_oszlopok = ["Aktív fertőzött", "Elhunyt", "Gyógyult", "Összesen", "Beoltottak", "Aktív fertőzöttek változása", "Napi új elhunyt", "Napi új gyógyult", "Napi új fertőzött", "Napi új beoltott"]
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

csvout.to_csv(DATADIR +"/covidadatok.csv", index = False)

csv = pd.read_csv(DATADIR +"/covidadatok.csv")

csvpart = csv[["Dátum", "Elhunyt"]]

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

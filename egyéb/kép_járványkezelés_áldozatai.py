#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from matplotlib import gridspec
from datetime import timedelta
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates

BASEDIR=os.path.dirname(__file__)

KATEGORIA = ["0-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80-84","85-89", "90-"]

def kategoriaSzamolo(c):
    ct = int(c)
    if ct < 35:
        return "0-34"
    if ct >= 90:
        return "90-"
    
    ct = int(ct / 5) * 5
    return str(ct) + "-" + str(ct+4)

def kezdonapSzamolo(d):
    return d - dt.timedelta(days = d.weekday())

kezdet = "2020-04-01"
    
# KSH többlet

dfksh = pd.read_csv(BASEDIR +"/../adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
dfkshatlag = dfksh[dfksh['A hét záró napja'] < "2020-01-01"]
dfkshatlag = dfkshatlag.groupby('A hét sorszáma').mean().reset_index()

colnames = ["A hét sorszáma", "Összesen"]

for k in KATEGORIA:
    colname = k.replace("-","") + " éves összesen"
    newcolname = "átlag " + k  + " éves összesen"
    dfkshatlag = dfkshatlag.rename(columns = {colname: newcolname}, inplace = False)
    colnames.append(newcolname)
    
dfksh = dfksh[dfksh['A hét záró napja'] >= kezdet]

dfkshatlag = dfkshatlag[colnames].rename(columns = {"Összesen": "átlag összesen"}, inplace = False)
    
kezdonap = dfksh['A hét kezdő napja'].min()
zaronap = dfksh['A hét záró napja'].max()

dfkshmerge = pd.merge(dfksh, dfkshatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')

diffcolnames = ["A hét sorszáma", "A hét kezdő napja", "A hét záró napja", "diff összesen" ]

for k in KATEGORIA:
    colname = k.replace("-","") + " éves összesen"
    avgcolname = "átlag " + k  + " éves összesen"
    diffcolname = "diff " + k
    dfkshmerge[diffcolname] = dfkshmerge[colname] - dfkshmerge[avgcolname] + 0.5
    dfkshmerge[diffcolname] = dfkshmerge[diffcolname].astype(int)
    diffcolnames.append(diffcolname)

dfkshmerge['diff összesen'] = dfkshmerge["Összesen"] - dfkshmerge["átlag összesen"] + 0.5
dfkshmerge['diff összesen'] = dfkshmerge['diff összesen'].astype(int)
dfkshdiff = dfkshmerge[diffcolnames].sort_values('A hét kezdő napja')

df = pd.read_csv(BASEDIR +"/../adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= kezdonap]
df = df[df['Dátum'] <= zaronap]
    

df['Kategória'] = df.apply(lambda row:  kategoriaSzamolo(row['Kor']), axis=1)
df['A hét kezdő napja'] = df.apply(lambda row: kezdonapSzamolo(row['Dátum']), axis=1)

df = df.groupby(['A hét kezdő napja', 'Kategória'], as_index=False).count()
df = df[["A hét kezdő napja", "Kategória", "Sorszám"]].rename(columns = {"Sorszám": "COVID elhunyt"}, inplace = False)

for k in KATEGORIA:
    dfpart = df[df['Kategória'] == k].rename(columns = {"COVID elhunyt": "covid " + k}, inplace = False)
    dfpart = dfpart[['A hét kezdő napja', "covid " + k]]

    dfkshdiff = pd.merge(dfkshdiff, dfpart, left_on = 'A hét kezdő napja', right_on = 'A hét kezdő napja', how = 'left')

dfkshdiff = dfkshdiff.fillna(0)

num = dfkshdiff._get_numeric_data()
num[num < 0] = 0

dfkshdiff['Járványkezelés'] = [0] * len(dfkshdiff)

for k in KATEGORIA:
    dfkshdiff['covid ' + k] = dfkshdiff['covid ' + k].astype(int)
    dfkshdiff['jarvany ' + k] = dfkshdiff['diff ' + k] - dfkshdiff['covid ' + k]

num = dfkshdiff._get_numeric_data()
num[num < 0] = 0

aldozatsum = dfkshdiff.sum()

pite = []

for k in KATEGORIA:
   pite.append([k, aldozatsum['jarvany ' + k]])

dfpite = pd.DataFrame(pite, columns=['Korcsoport', 'Áldozat'])

colors = ['#00FF00', '#00E020', '#00C040', '#00B050', '#00A060', '#009070', '#008080', '#FFA0FF', '#FF80E0', '#FF60C0', 
          '#FF40A0', '#FF2080', '#FF0060' ]

explode = (0.35, 0.2, 0.15, 0.1, 0.06, 0.04, 0.02, 0, 0, 0, 0, 0, 0)

plot = dfpite.plot.pie(labels=dfpite['Korcsoport'], y='Áldozat', figsize=(9.5, 9.5), explode=explode, colors=colors, title='A COVID járványkezelés áldozatainak eloszlása Magyarországon',
                   autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/COVIDJárványkezelésÁldozatai.png", bbox_inches = "tight", dpi=80)

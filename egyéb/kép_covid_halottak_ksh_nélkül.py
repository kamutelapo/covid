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

def hetSzamolo(d):
    eleje = d - dt.timedelta(days = d.weekday()) - dt.timedelta(days = 3)
    if d < pd.to_datetime("2021-01-04") and d >= pd.to_datetime("2020-12-28"):
        return 53
    if d < pd.to_datetime("2020-12-28"):
        return int(eleje.strftime('%U')) + 2
    return int(eleje.strftime('%U')) + 1

# rajzolás
    
pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,7])

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         width_ratios=[1], wspace=0.3,
                         hspace=0.40, height_ratios=[1, 1])
spec.update(left=0.06,right=0.95,top=0.95,bottom=0.10,wspace=0.25,hspace=0.40)


formatter = mdates.DateFormatter("%Y-%m-%d")

for year in range(2020,2022):
    if year == 2020:
        kezdet = "2020-04-01"
        veg = "2021-01-01"
    if year == 2021:
        kezdet = "2021-01-01"
        veg = "2022-01-01"
    
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
    
    dfksh = dfksh[dfksh['A hét záró napja'] < veg]
    dfksh = dfksh[dfksh['A hét záró napja'] >= kezdet]

    dfkshatlag = dfkshatlag[colnames].rename(columns = {"Összesen": "átlag összesen"}, inplace = False)
    
    zaronap = dfksh['A hét záró napja'].max()
    kezdonap = dfksh['A hét kezdő napja'].min()

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
    dfkshdiff = dfkshmerge[diffcolnames]

    df = pd.read_csv(BASEDIR +"/../adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])
    df = df[df['Dátum'] >= kezdonap]
    df = df[df['Dátum'] <= zaronap]
    

    df['Kategória'] = df.apply(lambda row:  kategoriaSzamolo(row['Kor']), axis=1)
    df['A hét sorszáma'] = df.apply(lambda row: hetSzamolo(row['Dátum']), axis=1)

    #pd.set_option("display.max_rows", None)

    df = df.groupby(['A hét sorszáma', 'Kategória'], as_index=False).count()
    df = df[["A hét sorszáma", "Kategória", "Sorszám"]].rename(columns = {"Sorszám": "COVID elhunyt"}, inplace = False)


    for k in KATEGORIA:
        dfpart = df[df['Kategória'] == k].rename(columns = {"COVID elhunyt": "covid " + k}, inplace = False)
        dfpart = dfpart[['A hét sorszáma', "covid " + k]]

        dfkshdiff = pd.merge(dfkshdiff, dfpart, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma', how = 'left')

    dfkshdiff = dfkshdiff.fillna(0)

    num = dfkshdiff._get_numeric_data()
    num[num < 0] = 0


    dfkshdiff['KSH-ból hiányzik'] = [0] * len(dfkshdiff)

    for k in KATEGORIA:
        dfkshdiff['covid ' + k] = dfkshdiff['covid ' + k].astype(int)
        dfkshdiff['hiany ' + k] = dfkshdiff['covid ' + k] - dfkshdiff['diff ' + k]

    num = dfkshdiff._get_numeric_data()
    num[num < 0] = 0

    for k in KATEGORIA:
        dfkshdiff['KSH-ból hiányzik'] = dfkshdiff['KSH-ból hiányzik'] + dfkshdiff['hiany ' + k]


    meghaltvolna =  dfkshdiff['KSH-ból hiányzik'].sum()

    dfkshdiff['Dátum'] = dfkshdiff['A hét kezdő napja'] 

    maxhiany = 800

    ax10=fig.add_subplot(spec[year - 2020], label=str(year))
    ax10.plot(dfkshdiff['Dátum'], dfkshdiff['KSH-ból hiányzik'], color='blue', label="KSH-ból hiányzik")
    ax10.set_ylim([0,maxhiany])
    ax10.set_title(str(year) + " - COVID halottak, akik nem szerepelnek a KSH-ban (" + str(meghaltvolna) + " fő)", fontweight='bold')
    ax10.tick_params(axis='x', rotation=20)
    ax10.fill_between(dfkshdiff['Dátum'], dfkshdiff['KSH-ból hiányzik'], color="blue")
    ax10.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax10.xaxis.set_major_formatter(formatter)
    ax10.legend()

fig.savefig(BASEDIR + "/COVIDHalottakAkikNincsenekAKSHban.png")

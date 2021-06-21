#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

def isHealthy(c):
    lower = c.lower()
    return ('nem' in lower) and ('ismert' in lower)

df = pd.read_csv(BASEDIR +"/elhunytak_datummal.csv", parse_dates=['Dátum'])

df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfhetimind = df.groupby('Hét kezdet', as_index=False).count()
dffiltered = dfhetimind[['Hét kezdet', 'Sorszám']].rename(columns = {'Sorszám': 'Heti összes'}, inplace = False)

df = pd.merge(df, dffiltered, left_on = 'Hét kezdet', right_on = 'Hét kezdet')
df = df[np.vectorize(isHealthy)(df['Alapbetegségek'])].reset_index()

dfheti = (df.groupby('Hét kezdet', as_index=False).agg(['mean', 'count'], as_index = False))
dfheti = dfheti['Heti összes'].reset_index().rename(columns = {'Hét kezdet': 'Dátum', 'mean': 'Heti halálozás / 10', 'count': 'Nem ismert alapbetegség'}, inplace = False)
dfheti['Heti halálozás / 10'] = dfheti['Heti halálozás / 10'] / 10

dfoltas = pd.read_csv(BASEDIR +"/covidadatok.csv", parse_dates=['Dátum'])
dfoltas['Hét kezdet'] = dfoltas.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfoltasmind = dfoltas.groupby('Hét kezdet', as_index=False).sum().reset_index()
dfoltasmind = dfoltasmind[['Hét kezdet', 'Napi új beoltott']].rename(columns = {'Hét kezdet': 'Dátum', 'Napi új beoltott': 'Heti új beoltott / 1500'}, inplace = False)
dfoltasmind['Heti új beoltott / 1500'] = dfoltasmind['Heti új beoltott / 1500'] / 1500

dfheti = pd.merge(dfheti, dfoltasmind, left_on = 'Dátum', right_on = 'Dátum')


plot = dfheti.plot(x='Dátum', y=['Heti halálozás / 10', 'Nem ismert alapbetegség', 'Heti új beoltott / 1500'])	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/NemIsmertAlapbetegség.png", bbox_inches = "tight", dpi = 300)

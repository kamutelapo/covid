#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kező napja', 'A hét záró napja'], delimiter=';')
dfweeks = df[(df['A hét sorszáma'] < 23.0) | (df['A hét sorszáma'] > 35.0)]

df2020 = dfweeks[dfweeks['A hét záró napja'] > "2020-08-30"]
covid_elhunytak = df2020[['A hét kező napja', 'A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'Elhunytak'}, inplace = False)

dfatlag = dfweeks[dfweeks['A hét záró napja'] < "2020-01-01"]

dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()
atlag_elhunytak = dfatlag[['A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'KSH 5 éves átlag'}, inplace = False)

dfkozos = pd.merge(covid_elhunytak, atlag_elhunytak, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkozos = dfkozos.rename(columns = {'A hét kező napja': 'Dátum'}, inplace = False)
dfkozos['KSH többlet']=dfkozos['Elhunytak'] - dfkozos['KSH 5 éves átlag']

diff = int(dfkozos['KSH többlet'].sum() + 0.5)

if (diff > 0):
    diff = "+" + str(diff)
else:
    diff = str(diff)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df['Dátum'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfheti = (df.groupby('Dátum', as_index=False).sum())
dfheti['Hivatalos heti új elhunyt'] = dfheti['Napi új elhunyt']
dfheti = dfheti[(dfheti['Dátum'] < "2021-06-01") & (dfheti['Dátum'] > "2020-08-30")]

dfkozos = pd.merge(dfkozos, dfheti, left_on = 'Dátum', right_on = 'Dátum')

plot = dfkozos.plot(x='Dátum', y=['Hivatalos heti új elhunyt', 'KSH többlet'], title='COVID halálozási többlet az 5 éves KSH átlag alapján (' + diff + ' fő)')
plot.axhline(0,color='magenta',ls='--')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KshVsHivatalosCovidHalálozás.png", bbox_inches = "tight")

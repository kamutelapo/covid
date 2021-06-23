#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kező napja', 'A hét záró napja'], delimiter=';')
dfweeks = df[(df['A hét sorszáma'] < 21.0) | (df['A hét sorszáma'] > 35.0)]

df2020 = dfweeks[dfweeks['A hét záró napja'] > "2020-08-30"]
covid_elhunytak = df2020[['A hét kező napja', 'A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'Elhunytak'}, inplace = False)

dfatlag = dfweeks[dfweeks['A hét záró napja'] < "2020-01-01"]

dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()
atlag_elhunytak = dfatlag[['A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'KSH 5 éves átlag'}, inplace = False)

dfkozos = pd.merge(covid_elhunytak, atlag_elhunytak, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkozos = dfkozos.rename(columns = {'A hét kező napja': 'Dátum'}, inplace = False)
dfkozos['Többlet']=dfkozos['Elhunytak'] - dfkozos['KSH 5 éves átlag']

diff = int(dfkozos['Többlet'].sum() + 0.5)

if (diff > 0):
    diff = "+" + str(diff)
else:
    diff = str(diff)

plot = dfkozos.plot(x='Dátum', y=['Többlet'], title='COVID halálozási többlet a KSH átlag alapján (' + diff + ' fő)')
plot.axhline(0,color='magenta',ls='--')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KshCovidHalálozásiTöbblet.png", bbox_inches = "tight")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from datetime import timedelta

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
maxdate = df['A hét kezdő napja'].max() + timedelta(days = -35)
df = df[df['A hét kezdő napja'] <= maxdate]

df2020 = df[df['A hét záró napja'] > "2020-08-30"]
covid_elhunytak = df2020[['A hét kezdő napja', 'A hét sorszáma', 'Összesen']].rename(columns = {'Összesen': 'Elhunytak'}, inplace = False)

dfatlag = df[df['A hét záró napja'] < "2020-01-01"]

dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()
atlag_elhunytak = dfatlag[['A hét sorszáma', 'Összesen']].rename(columns = {'Összesen': 'KSH 5 éves átlag'}, inplace = False)

dfkozos = pd.merge(covid_elhunytak, atlag_elhunytak, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkozos = dfkozos.rename(columns = {'A hét kezdő napja': 'Dátum'}, inplace = False)
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

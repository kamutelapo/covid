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
df2020['2020/21 elhunytak'] = df2020['034 éves összesen'] + df2020['3539 éves összesen']
covid_elhunytak = df2020[['A hét kezdő napja', 'A hét sorszáma', '2020/21 elhunytak']]

dfatlag = df[df['A hét záró napja'] < "2020-01-01"]

dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()
dfatlag['Elhunytak'] = dfatlag['034 éves összesen'] + dfatlag['3539 éves összesen']
atlag_elhunytak = dfatlag[['A hét sorszáma', 'Elhunytak']].rename(columns = {'Elhunytak': 'KSH 5 éves átlag'}, inplace = False)

dfkozos = pd.merge(covid_elhunytak, atlag_elhunytak, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkozos = dfkozos.rename(columns = {'A hét kezdő napja': 'Dátum'}, inplace = False)
dfkozos['Többlet']=dfkozos['2020/21 elhunytak'] - dfkozos['KSH 5 éves átlag']
diff = int(dfkozos['Többlet'].sum() + 0.5)

if (diff > 0):
    diff = "+" + str(diff)
else:
    diff = str(diff)

plot = dfkozos.plot(x='Dátum', y=['Többlet'], title='40 év alattiak COVID halálozási többlete KSH átlag alapján (' + diff + ' fő)')
plot.axhline(0,color='magenta',ls='--')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/FiatalokCovidHalálozásiTöbblete.png", bbox_inches = "tight")

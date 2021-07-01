#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt

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

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df['Dátum'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfheti = (df.groupby('Dátum', as_index=False).sum())

dfheti = dfheti.rename(columns = {'Napi új beoltott': 'Heti új beoltott'}, inplace = False)
dfheti = dfheti[(dfheti['Dátum'] < "2021-06-01") & (dfheti['Dátum'] > "2020-08-30")]

dfkozos = pd.merge(dfkozos, dfheti, left_on = 'Dátum', right_on = 'Dátum')


pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_title("COVID halálozások vs oltások")
host.set_ylabel("KSH többlet")
host.set_ylim([-250, 5500])
par.set_ylabel("Heti új beoltott")
par.set_ylim([-25000, 550000])

p1, = host.plot(dfkozos['Dátum'], dfkozos['KSH többlet'], label="KSH többlet", color='blue')
p2, = par.plot(dfkozos['Dátum'], dfkozos['Heti új beoltott'], label="Heti új beoltott", color='green')

leg = plt.legend(loc='upper left')

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

host.axhline(0,color='magenta',ls='--')

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/KshHalálozásVsOltás.png", bbox_inches = "tight")

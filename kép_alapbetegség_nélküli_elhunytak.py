#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

BASEDIR=os.path.dirname(__file__)

def isHealthy(c):
    lower = c.lower()
    return ('nem' in lower) and ('ismert' in lower)

df = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])

df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfhetimind = df.groupby('Hét kezdet', as_index=False).count()
dffiltered = dfhetimind[['Hét kezdet', 'Sorszám']].rename(columns = {'Sorszám': 'Heti összes'}, inplace = False)

df = pd.merge(df, dffiltered, left_on = 'Hét kezdet', right_on = 'Hét kezdet')
df = df[np.vectorize(isHealthy)(df['Alapbetegségek'])].reset_index()

dfheti = (df.groupby('Hét kezdet', as_index=False).agg(['mean', 'count'], as_index = False))
dfheti = dfheti['Heti összes'].reset_index().rename(columns = {'Hét kezdet': 'Dátum', 'mean': 'Heti halálozás', 'count': 'Nem ismert alapbetegség'}, inplace = False)

dfoltas = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
dfoltas['Hét kezdet'] = dfoltas.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfoltasmind = dfoltas.groupby('Hét kezdet', as_index=False).sum().reset_index()
dfoltasmind = dfoltasmind[['Hét kezdet', 'Napi új beoltott']].rename(columns = {'Hét kezdet': 'Dátum', 'Napi új beoltott': 'Heti új beoltott'}, inplace = False)

dfheti = pd.merge(dfheti, dfoltasmind, left_on = 'Dátum', right_on = 'Dátum')

pd.plotting.register_matplotlib_converters()

host = host_subplot(111, axes_class=AA.Axes)

par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))
par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)

host.set_xlabel("Dátum")
host.set_title("Alapbetegség nélküli COVID elhunytak")
host.set_ylabel("Heti halálozás")
host.set_ylim([-80, 4000])
par1.set_ylabel("Nem ismert alapbetegség")
par1.set_ylim([-8, 400])
par2.set_ylabel("Heti új beoltott")
par2.set_ylim([-11000, 550000])

p1, = host.plot(dfheti['Dátum'], dfheti['Heti halálozás'], label="Heti halálozás")
p2, = par1.plot(dfheti['Dátum'], dfheti['Nem ismert alapbetegség'], label="Nem ismert alapbetegség")
p3, = par2.plot(dfheti['Dátum'], dfheti['Heti új beoltott'], label="Heti új beoltott")

leg = plt.legend(loc='upper left')

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par1.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

par2.yaxis.get_label().set_color(p3.get_color())
leg.texts[2].set_color(p3.get_color())

host.axhline(0, color='black', ls='--', linewidth=1)

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/NemIsmertAlapbetegség.png", bbox_inches = "tight", dpi = 100)

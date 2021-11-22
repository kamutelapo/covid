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

dfcv = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
dfcv = dfcv[dfcv['Dátum'] >= "2020-07-01"].reset_index()
dfcvroll = dfcv.rolling(7, center=True, min_periods=7).sum()
dfcv['Heti halálozás'] = dfcvroll['Napi új elhunyt']
dfcv['Heti új oltott'] = dfcvroll['Napi új beoltott'] + dfcvroll['Napi új másodszor oltott']

df = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])
df = df[np.vectorize(isHealthy)(df['Alapbetegségek'])].reset_index()
df = df[df['Dátum'] >= "2020-07-01"].reset_index()
dfnapimind = df.groupby('Dátum', as_index=False).count()
dfnapimind = dfnapimind[['Dátum','Alapbetegségek']].rename(columns = {'Alapbetegségek': 'Napi nem ismert alapbetegség'}, inplace = False)

df = pd.merge(dfcv[['Dátum']], dfnapimind, left_on = 'Dátum', right_on = 'Dátum', how="outer").fillna(0)
dfroll = df.rolling(7, center=True, min_periods=7).sum()
df['Nem ismert alapbetegség'] = dfroll['Napi nem ismert alapbetegség']

df = pd.merge(dfcv, df, left_on = 'Dátum', right_on = 'Dátum', how="outer")

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
host.set_ylim([0, 4000])
host.axis[:].major_ticks.set_tick_out(True)
host.axis["top"].major_ticks.set_visible(False)
host.axis["bottom"].major_ticklabels.set_rotation(15)
par1.set_ylabel("Nem ismert alapbetegség")
par1.set_ylim([0, 400])
par1.axis[:].major_ticks.set_tick_out(True)
par2.set_ylabel("Heti új oltott (1x+2x)")
par2.set_ylim([0, 900000])
par2.axis[:].major_ticks.set_tick_out(True)

p1, = host.plot(df['Dátum'], df['Heti halálozás'], label="Heti halálozás")
p2, = par1.plot(df['Dátum'], df['Nem ismert alapbetegség'], label="Nem ismert alapbetegség")
p3, = par2.plot(df['Dátum'], df['Heti új oltott'], label="Heti új oltott (1x+2x)")

leg = plt.legend(loc='upper left')

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par1.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

par2.yaxis.get_label().set_color(p3.get_color())
leg.texts[2].set_color(p3.get_color())

fig = host.get_figure()
fig.savefig(BASEDIR + "/képek/NemIsmertAlapbetegség.png", bbox_inches = "tight", dpi = 100)

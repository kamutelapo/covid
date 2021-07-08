#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt

BASEDIR=os.path.dirname(__file__)

# fertőzés utáni várható halál 20 nap
VARHATO_HALAL=20

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= "2020-08-01"].reset_index()

fertozott = df.iloc[:-VARHATO_HALAL]
ujelhunyt = df.iloc[VARHATO_HALAL:, :]['Napi új elhunyt'].reset_index()
fertozott['Fertőzésben meghalt'] = ujelhunyt['Napi új elhunyt']

dfheti = fertozott.rolling(7, center=True, min_periods=4).mean()
dfheti['Fertőzésben meghalt'] = dfheti.apply(lambda row: row['Fertőzésben meghalt'] if int(row['Fertőzésben meghalt']) >= 15 else np.NaN, axis=1)
fertozott['Heti új fertőzöttek átlaga'] = dfheti['Napi új fertőzött']
fertozott['Heti új elhunytak átlaga'] = dfheti['Fertőzésben meghalt']
dfheti = fertozott

dfheti['Halálozási ráta'] = dfheti['Heti új elhunytak átlaga'] / dfheti['Heti új fertőzöttek átlaga']

pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Halálozási ráta")
host.set_title("COVID fertőzöttek halálozási rátája (halálozás " + str(VARHATO_HALAL) + " nappal eltolva)")
par.set_ylabel("Heti új fertőzött átlaga")
par.set_ylim([0, 80000])

p1, = host.plot(dfheti['Dátum'], dfheti['Halálozási ráta'], label="Halálozási ráta")
p2, = par.plot(dfheti['Dátum'], dfheti['Heti új fertőzöttek átlaga'], label="Heti új fertőzöttek átlaga")

leg = plt.legend()

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/FertőzöttekHalálozásiRátája.png", bbox_inches = "tight")


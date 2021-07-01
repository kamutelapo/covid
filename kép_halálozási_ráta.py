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

fertozott = df.iloc[:-VARHATO_HALAL]
ujelhunyt = df.iloc[VARHATO_HALAL:, :]['Napi új elhunyt'].reset_index()
fertozott['Fertőzésben meghalt'] = ujelhunyt['Napi új elhunyt']

fertozott['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfheti = (fertozott.groupby('Hét kezdet', as_index=False).mean())
dfheti['Fertőzésben meghalt'] = dfheti.apply(lambda row: row['Fertőzésben meghalt'] if int(row['Fertőzésben meghalt']) >= 15 else np.NaN, axis=1)
dfheti['Halálozási ráta'] = dfheti['Fertőzésben meghalt'] / dfheti['Napi új fertőzött']
dfheti = dfheti.rename(columns = {'Hét kezdet': 'Dátum', 'Napi új fertőzött': 'Heti új fertőzött átlaga'}, inplace = False)

pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Halálozási ráta")
host.set_title("COVID fertőzöttek halálozási rátája (halálozás " + str(VARHATO_HALAL) + " nappal eltolva)")
par.set_ylabel("Heti új fertőzött átlaga")
par.set_ylim([0, 80000])

p1, = host.plot(dfheti['Dátum'], dfheti['Halálozási ráta'], label="Halálozási ráta")
p2, = par.plot(dfheti['Dátum'], dfheti['Heti új fertőzött átlaga'], label="Heti új fertőzött átlaga")

leg = plt.legend()

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/FertőzöttekHalálozásiRátája.png", bbox_inches = "tight")


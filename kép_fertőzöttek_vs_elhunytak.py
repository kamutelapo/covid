#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt


BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfheti = (df.groupby('Hét kezdet', as_index=False).mean())
dfheti['Heti új fertőzöttek átlaga'] = dfheti['Napi új fertőzött']
dfheti['Heti új elhunytak átlaga'] = dfheti['Napi új elhunyt']
dfheti['Dátum'] = dfheti['Hét kezdet']

pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Heti új fertőzöttek átlaga")
host.set_title("COVID fertőzöttek és elhunytak")
par.set_ylabel("Heti új elhunytak átlaga")
par.set_ylim([0, 450])

p1, = host.plot(dfheti['Dátum'], dfheti['Heti új fertőzöttek átlaga'], label="Heti új fertőzöttek átlaga")
p2, = par.plot(dfheti['Dátum'], dfheti['Heti új elhunytak átlaga'], label="Heti új elhunytak átlaga")

leg = plt.legend()

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/FertőzöttekVsElhunytak.png", bbox_inches = "tight")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')
dfheti = df.rolling(7, center=True, min_periods=4).mean()
df['Heti új fertőzöttek átlaga'] = dfheti['Napi új fertőzött']

pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Heti új fertőzöttek átlaga")
host.set_title("Új fertőzöttek és kórházban ápoltak")
host.set_ylim([0, 10000])
par.set_ylabel("Kórházban ápoltak")
par.set_ylim([0, 14000])

p1, = host.plot(df['Dátum'], df['Heti új fertőzöttek átlaga'], label="Heti új fertőzöttek átlaga", color='red')
p2, = par.plot(df['Dátum'], df['Kórházban ápoltak'], label="Kórházban ápoltak", color='blue')

leg = plt.legend()

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/KórházbanÁpoltakVsÚjFertőzöttek.png", bbox_inches = "tight")

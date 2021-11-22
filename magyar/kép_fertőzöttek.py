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

df = pd.read_csv(BASEDIR +"/újfertőzések.csv", parse_dates=['Dátum'])
df["Oltottak aránya"] =100 * df['Legalább 1 oltással rendelkezők száma'] / df['Regisztrált fertőzöttek száma']

summa = df.sum()

rate = int(100.0 * summa['Legalább 1 oltással rendelkezők száma'] / summa['Regisztrált fertőzöttek száma'] + 0.5)


pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Új fertőzöttek")
host.set_title("Magyar COVID adatok az új fertőzöttekről (" + str(rate) + "% oltott)")
host.set_ylim([0, 5000])
par.set_ylabel("Oltottak aránya")
par.set_ylim([0, 100])

p1, = host.plot(df['Dátum'], df['Regisztrált fertőzöttek száma'], label="Regisztrált fertőzöttek száma", color="#7070FF")
p1b, = host.plot(df['Dátum'], df['Legalább 1 oltással rendelkezők száma'], label="Legalább 1 oltással rendelkezők száma", color="darkblue")
p2, = par.plot(df['Dátum'], df['Oltottak aránya'], label="Oltottak aránya", color="magenta")

host.fill_between(df['Dátum'], df['Regisztrált fertőzöttek száma'], color="#7070FF")
host.fill_between(df['Dátum'], df['Legalább 1 oltással rendelkezők száma'], color="darkblue")

leg = plt.legend()

host.yaxis.get_label().set_color(p1b.get_color())
leg.texts[0].set_color(p1.get_color())

leg.texts[1].set_color(p1b.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[2].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/Fertőzöttek.png", bbox_inches = "tight")

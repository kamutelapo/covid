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

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
dfheti = df.rolling(7, center=True, min_periods=4).mean()
df['Heti új elhunytak átlaga'] = dfheti['Napi új elhunyt']
df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')
df = df[df['Dátum'] >= "2020-04-17"]

korrelacio = []
dfek = []

for napok in range(0,15):
    if napok == 0:
        c1 = df
        c2 = df
    else:
        c1 = df.iloc[napok:, :]['Heti új elhunytak átlaga'].reset_index()
        c2 = df.iloc[:-napok].reset_index()

    dfr = c1[['Heti új elhunytak átlaga']]
    dfr['Lélegeztetettek'] = c2['Lélegeztetettek']
    dfr['Dátum'] = c2['Dátum']
    
    korrelacio.append([napok, dfr['Lélegeztetettek'].corr(dfr['Heti új elhunytak átlaga'])])
    dfek.append(dfr)
    

dfkorr = pd.DataFrame(korrelacio, columns=['Napok eltolása', 'Korreláció'])

dfsorted=dfkorr.sort_values('Korreláció', ascending=False)

varhato_halal = int(dfsorted['Napok eltolása'].head(1).mean())


dfr = dfek[varhato_halal]

pd.plotting.register_matplotlib_converters()

host = host_subplot(211, axes_class=AA.Axes)

host.set_xlabel("Napok")
host.set_ylabel("Korreláció")
host.set_title("Lélegeztetés után várható halál (" + str(varhato_halal) + " nap)")
host.axis["top"].major_ticks.set_visible(False)
host.axis["right"].major_ticks.set_visible(False)

hostp, = host.plot(dfkorr['Napok eltolása'], dfkorr['Korreláció'], label="Korreláció", color = 'green', marker='o')

leg = host.legend(loc='upper right')

host.yaxis.get_label().set_color(hostp.get_color())
leg.texts[0].set_color(hostp.get_color())

par = host_subplot(212)
par.set_xlabel("Dátum")
par.set_title("Lélegeztetés, korreláció " + str(varhato_halal) + " napos eltolással" )
par.get_yaxis().set_visible(False)

parp1, = par.plot(dfr['Dátum'], dfr['Lélegeztetettek'] / 3.5, label="Lélegeztetettek")
parp2, = par.plot(dfr['Dátum'], dfr['Heti új elhunytak átlaga'], label="Heti új elhunytak átlaga")

leg2 = par.legend(loc='upper left')

fig = host.get_figure()
fig.set_figheight(8)
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/LélegeztetésUtánVárhatóHalál.png", bbox_inches = "tight")
    
plt.clf()

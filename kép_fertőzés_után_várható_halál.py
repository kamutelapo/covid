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

hullamok = [ [2, "Második"], [3, "Harmadik"]]

for hullam in (hullamok):
    hullamszam = hullam[0]
    hullamnev = hullam[1]
    
    df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
    
    if hullamszam == 2:
        df = df[df['Dátum'] >= "2020-08-01"]
        df = df[df['Dátum'] < "2021-02-01"]
    else:
        df = df[df['Dátum'] >= "2021-01-31"]
    

    korrelacio = []
    dfek = []

    for napok in range(0,30):
        if napok == 0:
            c1 = df
            c2 = df
        else:
            c1 = df.iloc[napok:, :]['Napi új elhunyt'].reset_index()
            c2 = df.iloc[:-napok].reset_index()

        dfr = c1[['Napi új elhunyt']]
        dfr['Napi új fertőzött'] = c2['Napi új fertőzött']
        dfr['Dátum'] = c2['Dátum']
    
        korrelacio.append([napok, dfr['Napi új fertőzött'].corr(dfr['Napi új elhunyt'])])
        dfek.append(dfr)
    

    dfkorr = pd.DataFrame(korrelacio, columns=['Napok eltolása', 'Korreláció'])

    dfsorted=dfkorr.sort_values('Korreláció', ascending=False)

    varhato_halal = int(dfsorted['Napok eltolása'].head(1).mean())
    
    if hullamszam == 3:
      varhato_halal = 19 # szebben korrelál

    dfr = dfek[varhato_halal]
    dfrheti = dfr.rolling(7, center=True, min_periods=4).mean()
    dfr['Heti új fertőzöttek átlaga'] = dfrheti['Napi új fertőzött']
    dfr['Heti új elhunytak átlaga'] = dfrheti['Napi új elhunyt']

    pd.plotting.register_matplotlib_converters()

    host = host_subplot(211, axes_class=AA.Axes)

    host.set_xlabel("Napok")
    host.set_ylabel("Korreláció")
    host.set_title(hullamnev + " hullám, fertőzés után várható halál (" + str(varhato_halal) + " nap)")
    host.axis["top"].major_ticks.set_visible(False)
    host.axis["right"].major_ticks.set_visible(False)

    hostp, = host.plot(dfkorr['Napok eltolása'], dfkorr['Korreláció'], label="Korreláció", color = 'green')

    leg = host.legend(loc='upper left')

    host.yaxis.get_label().set_color(hostp.get_color())
    leg.texts[0].set_color(hostp.get_color())

    par = host_subplot(212)
    par.set_xlabel("Dátum")
    par.set_title(hullamnev + " hullám, korreláció " + str(varhato_halal) + " napos eltolással" )
    par.get_yaxis().set_visible(False)

    parp1, = par.plot(dfr['Dátum'], dfr['Heti új fertőzöttek átlaga'] / 20, label="Heti új fertőzöttek átlaga")
    parp2, = par.plot(dfr['Dátum'], dfr['Heti új elhunytak átlaga'], label="Heti új elhunytak átlaga")

    if hullamszam == 2:
        leg2 = par.legend(loc='upper left')
    else:
        leg2 = par.legend(loc='upper right')


    fig = host.get_figure()
    fig.set_figheight(8)
    fig.autofmt_xdate()
    fig.savefig(BASEDIR + "/képek/FertőzésUtánVárhatóHalál" + str(hullamszam) + ".png", bbox_inches = "tight")
    
    plt.clf()

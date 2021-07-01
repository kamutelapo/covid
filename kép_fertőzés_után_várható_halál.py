#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= "2020-08-01"]
df = df[df['Dátum'] < "2021-02-01"]

korrelacio = []

for napok in range(0,30):
    if napok == 0:
      c1 = df
      c2 = df
    else:
      c1 = df.iloc[napok:, :]['Napi új elhunyt'].reset_index()
      c2 = df.iloc[:-napok]['Napi új fertőzött'].reset_index()

    dfr = c1[['Napi új elhunyt']]
    dfr['Napi új fertőzött'] = c2['Napi új fertőzött']
    
    korrelacio.append([napok, dfr['Napi új fertőzött'].corr(dfr['Napi új elhunyt'])])
    

dfkorr = pd.DataFrame(korrelacio, columns=['Napok eltolása', 'Korreláció'])

dfsorted=dfkorr.sort_values('Korreláció', ascending=False)

varhato_halal = int(dfsorted['Napok eltolása'].head(1).mean())

plot = dfkorr.plot(x='Napok eltolása', y='Korreláció', title="COVID fertőzés után várható halál (" + str(varhato_halal) + " nap)")	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/FertőzésUtánVárhatóHalál.png", bbox_inches = "tight")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')

elozoertek = df.iloc[:-1]['Kórházban ápoltak']
elsonan = pd.DataFrame([[np.NaN]]);

elozoertek = pd.concat([elsonan, elozoertek], ignore_index=True)
elozoertek.columns = ['Kórházban ápoltak']

df['Kórházban ápoltak változása'] = df['Kórházban ápoltak'] - elozoertek['Kórházban ápoltak']

dfavg = df.rolling(7, center=True, min_periods=4).mean()

df['Kórházban ápoltak változása'] = dfavg['Kórházban ápoltak változása']

plot = df.plot(x='Dátum', y='Kórházban ápoltak változása', title='A COVID miatt kórházban ápoltak számának változása')
plot.axhline(0,color='magenta',ls='--')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KórházbanÁpoltakVáltozása.png", bbox_inches = "tight")

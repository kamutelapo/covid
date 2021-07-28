#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
dfheti = df.rolling(7, center=True, min_periods=4).mean()
df['Heti új fertőzöttek átlaga'] = dfheti['Napi új fertőzött']

elozoertek = df.iloc[:-7]['Heti új fertőzöttek átlaga']
elsonan = pd.DataFrame([[np.NaN]] * 7);
elozoertek = pd.concat([elsonan, elozoertek], ignore_index=True)
elozoertek.columns = ['Előző fertőzött átlag']

df['Előző fertőzött átlag'] = elozoertek['Előző fertőzött átlag']
df['Terjedés'] = df['Heti új fertőzöttek átlaga'] / df['Előző fertőzött átlag']

plot = df.plot(x='Dátum', y='Terjedés', title="Fertőzöttek számának növekedése az előző héthez képest")	
plot.axhline(1.0,color='magenta',ls='--')


fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/VírusTerjedés.png", bbox_inches = "tight")

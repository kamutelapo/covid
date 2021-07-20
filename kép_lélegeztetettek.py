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
df2 = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])

dfkozos = pd.merge(df, df2, left_on = 'Dátum', right_on = 'Dátum', how='outer')
dfkozos = dfkozos[dfkozos['Dátum'] >= "2020-04-17"]
dfkozos = dfkozos[dfkozos['Dátum'] < "2021-07-01"]

dfkozos['Lélegeztetettek'] = dfkozos['Lélegeztetettek'].interpolate(method='linear')


plot = dfkozos.plot(x='Dátum', y='Lélegeztetettek', title="Lélegeztetettek száma")	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Lélegeztetettek.png", bbox_inches = "tight")

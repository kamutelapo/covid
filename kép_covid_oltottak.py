#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= "2021-01-01"].reset_index()

dfheti = df.rolling(7, center=True, min_periods=4).mean()
df['Heti új beoltottak átlaga'] = dfheti['Napi új beoltott']
df['Heti új másodszor oltottak átlaga'] = dfheti['Napi új másodszor oltott']

plot = df.plot(x='Dátum', y=['Heti új beoltottak átlaga', 'Heti új másodszor oltottak átlaga'], ylim=[0, 100000], title='A COVID ellen beoltottak számának heti átlaga', color=['darkblue', 'red'])

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Beoltottak.png", bbox_inches = "tight")

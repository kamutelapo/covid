#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])

dfheti = df.rolling(7, center=True, min_periods=4).mean()
df['Heti új beoltottak átlaga'] = dfheti['Napi új beoltott']

plot = df.plot(x='Dátum', y='Heti új beoltottak átlaga', title='A COVID ellen beoltottak számának heti átlaga')	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Beoltottak.png", bbox_inches = "tight")

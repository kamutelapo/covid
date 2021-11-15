#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= "2021-01-01"].reset_index()

df['6 hónapon belül oltottak'] = ((df['Napi új másodszor oltott'] + df['Napi új harmadszor oltott']).rolling(min_periods=1, window=182).sum().fillna(0))


plot = df.plot(x='Dátum', y=['6 hónapon belül oltottak', 'Beoltottak', 'Kétszer oltottak', 'Háromszor oltottak'],
               ylim=[0, 6000000], title='A COVID ellen beoltottak összesen', color=['magenta', 'blue', 'orange', 'green'],
               grid=True)

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/BeoltottakÖsszesen.png", bbox_inches = "tight")

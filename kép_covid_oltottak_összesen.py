#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df = df[df['Dátum'] >= "2021-01-01"].reset_index()

plot = df.plot(x='Dátum', y=['Beoltottak', 'Kétszer oltottak'], ylim=[0, 6000000], title='A COVID ellen beoltottak összesen', color=['blue', 'orange'], grid=True)

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/BeoltottakÖsszesen.png", bbox_inches = "tight")

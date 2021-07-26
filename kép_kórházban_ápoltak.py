#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')

plot = df.plot(x='Dátum', y='Kórházban ápoltak', ylim=[0, 13000], title='A COVID miatt kórházban ápoltak száma')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KórházbanÁpoltak.png", bbox_inches = "tight")

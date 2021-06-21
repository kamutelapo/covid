#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/covidadatok.csv", parse_dates=['Dátum'])
df['Napi új beoltott'] = df['Napi új beoltott'].astype(float)
df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfheti = (df.groupby('Hét kezdet', as_index=False).mean())
dfheti['Heti új beoltottak átlaga'] = dfheti['Napi új beoltott']
dfheti['Dátum'] = dfheti['Hét kezdet']

plot = dfheti.plot(x='Dátum', y='Heti új beoltottak átlaga')	


fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Beoltottak.png", bbox_inches = "tight")

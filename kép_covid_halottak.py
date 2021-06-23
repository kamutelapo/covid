#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfheti = (df.groupby('Hét kezdet', as_index=False).mean())
dfheti['Heti új elhunytak átlaga'] = dfheti['Napi új elhunyt']
dfheti['Dátum'] = dfheti['Hét kezdet']

plot = dfheti.plot(x='Dátum', y='Heti új elhunytak átlaga', title="A COVID halálozások heti átlaga")	


fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Halálozasok.png", bbox_inches = "tight")

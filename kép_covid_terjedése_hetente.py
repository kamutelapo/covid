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
dfheti['Heti új fertőzöttek átlaga'] = dfheti['Napi új fertőzött']
dfheti['Dátum'] = dfheti['Hét kezdet']


elozoertek = dfheti.iloc[:-1]['Heti új fertőzöttek átlaga']

elsonan = pd.DataFrame([[np.NaN]]);
elozoertek = pd.concat([elsonan, elozoertek], ignore_index=True)
elozoertek.columns = ['Előző fertőzött átlag']

dfheti['Előző fertőzött átlag'] = elozoertek['Előző fertőzött átlag']
dfheti['Terjedés'] = dfheti['Heti új fertőzöttek átlaga'] / dfheti['Előző fertőzött átlag']


plot = dfheti.plot(x='Dátum', y='Terjedés', title="Fertőzöttek számának növekedése az előző héthez képest")	
plot.axhline(1.0,color='magenta',ls='--')


fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/VírusTerjedés.png", bbox_inches = "tight")

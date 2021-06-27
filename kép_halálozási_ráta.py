#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

# fertőzés utáni várható halál 12 nap
VARHATO_HALAL=12

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])

fertozott = df.iloc[:-VARHATO_HALAL]
ujelhunyt = df.iloc[VARHATO_HALAL:, :]['Napi új elhunyt'].reset_index()
fertozott['Fertőzésben meghalt'] = ujelhunyt['Napi új elhunyt']

fertozott['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfheti = (fertozott.groupby('Hét kezdet', as_index=False).mean())
dfheti['Fertőzésben meghalt'] = dfheti.apply(lambda row: row['Fertőzésben meghalt'] if int(row['Fertőzésben meghalt']) >= 15 else np.NaN, axis=1)
dfheti['Halálozási ráta'] = dfheti['Fertőzésben meghalt'] / dfheti['Napi új fertőzött']
dfheti = dfheti.rename(columns = {'Hét kezdet': 'Dátum'}, inplace = False)
dfheti['Heti új fertőzött átlaga / 500000'] = dfheti['Napi új fertőzött'] / 500000
dfheti['Heti új elhunyt átlaga / 10000'] = dfheti['Napi új elhunyt'] / 10000

plot = dfheti.plot(x='Dátum', y=['Halálozási ráta', 'Heti új fertőzött átlaga / 500000'], title="COVID fertőzöttek halálozási rátája (halálozás 12 nappal eltolva)")	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/FertőzöttekHalálozásiRátája.png", bbox_inches = "tight")


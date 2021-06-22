#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/elhunytak_datummal.csv", parse_dates=['Dátum'])

df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfgrp = df.groupby('Hét kezdet')
dfhetihalott = dfgrp.size().to_frame('Heti elhunytak').reset_index()

dfkor = dfgrp.mean().reset_index()

dfkor = pd.merge(dfkor, dfhetihalott, left_on = 'Hét kezdet', right_on = 'Hét kezdet')

dfkor['Átlag életkor'] = dfkor.apply(lambda row: row['Kor'] if int(row['Heti elhunytak']) >= 10 else np.NaN, axis=1)

dfkor = dfkor.rename(columns = {'Hét kezdet': 'Dátum'}, inplace = False)

plot = dfkor.plot(x='Dátum', y='Átlag életkor')	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/ElhunytakÁtlagÉletkora.png", bbox_inches = "tight")

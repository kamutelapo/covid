#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])
dfgrp = df.groupby('Dátum').agg(['sum', 'count'])

dfgrp['Elhunyt'] = dfgrp[('Kor', 'count')]
dfgrp['Életkor összeg'] = dfgrp[('Kor', 'sum')]
del dfgrp['Sorszám']
del dfgrp['Nem']
del dfgrp['Alapbetegségek']
del dfgrp['Kor']

dfok = pd.DataFrame({'Dátum': pd.date_range(start=df['Dátum'].min(), end=df['Dátum'].max())})

dfgrp = pd.merge(dfgrp, dfok, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum').reset_index().fillna(0)
del dfgrp['index']

dfossz = dfgrp.rolling(7, center=True).sum()
dfgrp['Heti elhunyt'] = dfossz['Elhunyt'].fillna(0)
dfgrp['Átlag életkor'] = dfossz['Életkor összeg'] / dfossz['Elhunyt']
dfgrp['Átlag életkor'] = dfgrp.apply(lambda row: float(row['Átlag életkor']) if int(row['Heti elhunyt']) >= 13 else np.NaN, axis=1)

plot = dfgrp.plot(x='Dátum', y='Átlag életkor', title='A COVID-ban elhunytak átlag életkora')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/ElhunytakÁtlagÉletkora.png", bbox_inches = "tight")

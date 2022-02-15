#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt

BASEDIR=os.path.dirname(__file__)

avg = 75.9

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
dfgrp['Várható élettartam'] = dfgrp.apply(lambda row: avg, axis=1)
dfgrp = dfgrp.reset_index()

dfhir = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
dfheti = dfhir.rolling(7, center=True, min_periods=4).mean()
dfheti['Heti beoltottak száma'] = dfheti['Napi új beoltott'] + dfheti['Napi új másodszor oltott'] + dfheti['Napi új harmadszor oltott'] + dfheti['Napi új negyedszer oltott']
dfhir['Heti beoltottak száma'] = dfheti['Heti beoltottak száma'].copy()
dfhir = dfhir[['Dátum', 'Heti beoltottak száma']]

dfgrp = dfgrp.set_index('Dátum')
del dfgrp['index']

dfhir = dfhir.set_index('Dátum')
dfgrp = pd.merge(dfgrp, dfhir, left_index = True, right_index = True, how = 'left').sort_values('Dátum').reset_index()
dfgrp.rename(columns=''.join, inplace=True)

pd.plotting.register_matplotlib_converters()

host = host_subplot(111)

par = host.twinx()

host.set_xlabel("Dátum")
host.set_ylabel("Életkor")
host.set_title("Oltások és elhunytak átlag életkora")
#host.set_ylim([0, 17000])
par.set_ylabel("Beoltottak száma")
#par.set_ylim([0, 23800])

p1, = host.plot(dfgrp['Dátum'], dfgrp['Átlag életkor'], label="Átlag életkor", color='blue')
p1b, = host.plot(dfgrp['Dátum'], dfgrp['Várható élettartam'], label="Várható élettartam", color='#FF88FF')
p2, = par.plot(dfgrp['Dátum'], dfgrp['Heti beoltottak száma'], label="Heti beoltottak száma", color='green')

leg = plt.legend()

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())
leg.texts[1].set_color(p1b.get_color())

par.yaxis.get_label().set_color(p2.get_color())
leg.texts[2].set_color(p2.get_color())

fig = host.get_figure()
fig.autofmt_xdate()
fig.savefig(BASEDIR + "/képek/ElhunytakÁtlagÉletkoraVsOltottak.png", bbox_inches = "tight")

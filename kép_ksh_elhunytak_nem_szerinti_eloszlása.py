#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
import re

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kező napja', 'A hét záró napja'], delimiter=';')
dfweeks = df[(df['A hét sorszáma'] < 23.0) | (df['A hét sorszáma'] > 35.0)]

covid_elhunytak = dfweeks[dfweeks['A hét záró napja'] > "2020-08-30"].sum()

dfatlag = dfweeks[dfweeks['A hét záró napja'] < "2020-01-01"]
dfatlag = dfatlag.groupby('A hét sorszáma').mean().sum()
diff = covid_elhunytak - dfatlag

ferfiak = np.NaN
nok = np.NaN

for index, item in diff.iteritems():
    if index == 'Nő összesen':
        nok = int(item + 0.5)
    if index == 'Férfi összesen':
        ferfiak = int(item + 0.5)


data = [['Férfi', ferfiak], ['Nő', nok]];
df = pd.DataFrame(data, columns=['Nem', 'Halálozások'])

plot = df.plot.pie(labels=df['Nem'], y='Halálozások', title='KSH alapján a COVID elhunytak nem szerinti eloszlása',  autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KshElhunytakNemSzerint.png", bbox_inches = "tight")

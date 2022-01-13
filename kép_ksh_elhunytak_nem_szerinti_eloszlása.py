#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
import re
from datetime import timedelta

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
maxdate = df['A hét kezdő napja'].max() + timedelta(days = -35)
df = df[df['A hét kezdő napja'] <= maxdate]

covid_elhunytak = df[df['A hét záró napja'] > "2020-08-30"]

dfatlag = df[df['A hét záró napja'] < "2020-01-01"]
dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()

for index, item in dfatlag.iteritems():
    if ('Nő összesen' == index) or ('Férfi összesen' == index):
        dfatlag = dfatlag.rename(columns = {index: "Átlag " + index })

dfatlag = dfatlag[['A hét sorszáma', 'Átlag Nő összesen', 'Átlag Férfi összesen']]

diff = pd.merge(covid_elhunytak, dfatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma', how="left")

ferfiak = np.NaN
nok = np.NaN

for index, item in diff.iteritems():
    if index == 'Nő összesen':
        diff[index] = diff[index] - diff["Átlag " + index]
        nok = int(diff[index].sum() + 0.5)
    if index == 'Férfi összesen':
        diff[index] = diff[index] - diff["Átlag " + index]
        ferfiak = int(diff[index].sum() + 0.5)


data = [['Férfi', ferfiak], ['Nő', nok]];
df = pd.DataFrame(data, columns=['Nem', 'Halálozások'])

plot = df.plot.pie(labels=df['Nem'], y='Halálozások', title='KSH alapján a COVID elhunytak nem szerinti eloszlása',  autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KshElhunytakNemSzerint.png", bbox_inches = "tight")

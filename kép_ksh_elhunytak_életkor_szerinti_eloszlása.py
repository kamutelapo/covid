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
dfatlag = dfatlag.groupby('A hét sorszáma').mean()

for index, item in dfatlag.iteritems():
    if ' éves összesen' in index:
        name = "Átlag " + re.sub(str(b'\xc2\x96', 'utf-8'), '-', index)
        dfatlag = dfatlag.rename(columns = {index: name })

diff = pd.merge(covid_elhunytak, dfatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma', how="left")


korcsoport = []

for index, item in diff.iteritems():
    if (' éves összesen' in index) and ( 'Átlag' not in index):
        name = re.sub(str(b'\xc2\x96', 'utf-8'), '-', index)
        diff = diff.rename(columns = {index: name })

        diff[name] = diff[name] - diff["Átlag " + name]
        diff = diff.drop(["Átlag " + name], axis=1)


for index, item in diff.iteritems():
    if ' éves összesen' in index:
        name = re.sub(' éves összesen', '', index)

        korcsoport.append([name, item.sum()])

df = pd.DataFrame(korcsoport, columns=['Korcsoport', 'Többlet halálozás'])
tobblet = int(df['Többlet halálozás'].sum() + 0.5)

colors = ['#00FF00', '#00E020', '#00C040', '#00B050', '#00A060', '#009070', '#008080', '#FFA0FF', '#FF80E0', '#FF60C0', 
          '#FF40A0', '#FF2080', '#FF0060' ]

explode = (0.35, 0.2, 0.15, 0.1, 0.06, 0.04, 0.02, 0, 0, 0, 0, 0, 0)
df['Többlet halálozás'] = df['Többlet halálozás'].clip(lower = 0)

plot = df.plot.pie(labels=df['Korcsoport'], y='Többlet halálozás', figsize=(9.5, 9.5), explode=explode, colors=colors, title='KSH alapján a COVID elhunytak eloszlása Magyarországon ('
                   + str(tobblet) + ' fő)',  autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/KshElhunytakKorcsoportSzerint.png", bbox_inches = "tight", dpi=80)

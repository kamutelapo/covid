#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

BASEDIR=os.path.dirname(__file__)

def korcsoport(kor):
    kor = int(kor / 10) * 10
    if kor >= 90:
        return "90-"
    if kor < 20:
        return "-20"
    return str(kor) + "-" + str(kor+9)

df = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])

df['Korcsoport'] = df.apply(lambda row:  korcsoport(row['Kor']), axis=1)

dfkor = df.groupby('Korcsoport').size().to_frame('Halálozások')

colors = ['#00FF00', '#00C040', '#00A060', '#009070', '#008080', '#B03030',
          '#C02828', '#E02020', '#FF0000', ]

explode = (0.35, 0.2, 0.15, 0.1, 0.05, 0, 0, 0, 0)

plot = dfkor.plot.pie(y='Halálozások', figsize=(8.9, 8.9), explode=explode, colors=colors, title='COVID elhunytak eloszlása Magyarországon korcsoportok szerint',  autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/ElhunytakKorcsoportSzerint.png", bbox_inches = "tight", dpi=80)

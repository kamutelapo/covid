#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os

def nemEgyesites(nem):
    if nem == 'férfi':
        return 'Férfi'
    if nem == 'nõ':
        return 'Nő'
    if nem == 'Nõ':
        return 'Nő'
    return nem

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum'])

df['Nem'] = df.apply(lambda row:  nemEgyesites(row['Nem']), axis=1)

dfnem = df.groupby('Nem').size().to_frame('Halálozások')

plot = dfnem.plot.pie(y='Halálozások', title='COVID elhunytak nem szerinti eloszlása Magyarországon',  autopct='%.2f%%')

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/ElhunytakNemSzerint.png", bbox_inches = "tight")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import pandas as pd
from matplotlib import gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


def intervallumFormatter(x):
    return x + '. hét'

def hatasfokSzamolas(a,b):
    if (a == 0.0) or (b == 0.0):
        return np.NaN
    if ( a < b ):
        return -((a - b) / a) * 100
    return ((b - a) / b) * 100

def csoportNevek(dfdata):
    return list(dfdata.columns[1:])

def hatasfokTabla(dfdata, csoportok):
    dfmerge = None

    for csoport in csoportok:
        csopname = csoport
        if csopname == 'Under 18':
            csopname = '18 alatt'
        csopi = dfdata[dfdata['Korcsoport'] == csoport].rename(columns = {'Hatásfok': csopname} )
        csopi = csopi[['Intervallum', csopname]].set_index('Intervallum')
    
        if dfmerge is None:
            dfmerge = csopi
        else:
            dfmerge[csopname] = csopi[csopname]
    
    dfmerge = dfmerge.reset_index()
    return dfmerge

BASEDIR=os.path.dirname(__file__)
DATADIR=BASEDIR + "/adatok/"

COLORS = [
    '#00FF00', '#00C000', '#0000FF', '#0000C0', '#000080', '#FF0000', '#C00000', '#800000',
]

dfcases = pd.read_csv(DATADIR + "data-cases.csv")
dfemergency = pd.read_csv(DATADIR + "data-emergency.csv")
dfcases['Hatásfok'] = dfcases.apply(lambda row: hatasfokSzamolas(row['Kétszer oltottak aránya'], row['Oltatlanok aránya']), axis=1)
dfemergency['Hatásfok'] = dfemergency.apply(lambda row: hatasfokSzamolas(row['Kétszer oltottak aránya'], row['Oltatlanok aránya']), axis=1)

korcsoportok = dfcases['Korcsoport'].unique()

dfcaseseff = hatasfokTabla(dfcases, korcsoportok)
dfemergencyeff = hatasfokTabla(dfemergency, korcsoportok[1:])

    
pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[7,9], constrained_layout=True)

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         width_ratios=[1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1,1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("Védelem a fertőzés ellen")

ndx = 0
for csn in csoportNevek(dfcaseseff):
  ax1.plot(dfcaseseff['Intervallum'].apply(intervallumFormatter), dfcaseseff[csn], label=csn, marker='o', color = COLORS[ndx])
  ndx += 1
ax1.axhline(0.0,color='magenta',ls='--')
ax1.set(xlabel="Intervallum (hetek)", ylabel="Védelem az oltatlanokhoz képest")
ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
ax1.tick_params(axis='x', rotation=20)
ax1.set_ylim([-150, 350])
ax1.text(2, 320, '18 év alatt nagyon magas a hatásfok', color = 'red')
ax1.text(0, -140, 'A negatív hatásfok az oltatlanok előnyét jelenti', color = 'red')
ax1.legend()

ax2=fig.add_subplot(spec[1], label="2")

ax2.set_title("Védelem a kórházba kerülés ellen")

ndx = 0
for csn in csoportNevek(dfemergencyeff):
  ax2.plot(dfemergencyeff['Intervallum'].apply(intervallumFormatter), dfemergencyeff[csn], label=csn, marker='o', color = COLORS[ndx + 1])
  ndx += 1
ax2.axhline(0.0,color='magenta',ls='--')
ax2.set(xlabel="Intervallum (hetek)", ylabel="Védelem az oltatlanokhoz képest")
ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
ax2.tick_params(axis='x', rotation=20)
ax2.text(2.5, 700, '18 év alatt minimális a kórházi kezelés', color = 'red')
ax2.legend()


fig.suptitle('Brit COVID adatok\nA vakcinák hatásfoka', fontsize=22)
fig.savefig(BASEDIR + "/anglia-vakcinahatásfok.png")


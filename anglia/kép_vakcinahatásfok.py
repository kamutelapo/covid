#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import pandas as pd
from matplotlib import gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

BASEDIR=os.path.dirname(__file__)
DATADIR=BASEDIR + "/adatok/"

COLORS = [
    '#00FF00', '#00C000', '#0000FF', '#0000C0', '#000080', '#FF0000', '#C00000', '#800000',
]

dfcases = pd.read_csv(DATADIR + "data-cases.csv")

def intervallumFormatter(x):
    return x + '. hét'

def hatasfokSzamolas(a,b):
    if ( a < b ):
        return -((a - b) / a) * 100
    return ((b - a) / b) * 100

dfcases['Hatásfok'] = dfcases.apply(lambda row: hatasfokSzamolas(row['Kétszer oltottak aránya'], row['Oltatlanok aránya']), axis=1)

korcsoportok = dfcases['Korcsoport'].unique()
csopnevek = []

dfmerge = None

for csoport in korcsoportok:
    csopname = csoport
    if csopname == 'Under 18':
        csopname = '18 alatt'
    csopnevek.append(csopname)
    csopi = dfcases[dfcases['Korcsoport'] == csoport].rename(columns = {'Hatásfok': csopname} )
    csopi = csopi[['Intervallum', csopname]].set_index('Intervallum')
    
    if dfmerge is None:
        dfmerge = csopi
    else:
        dfmerge[csopname] = csopi[csopname]
    
dfmerge = dfmerge.reset_index()
    
pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[7,6], constrained_layout=True)

spec = gridspec.GridSpec(ncols=1, nrows=1,
                         width_ratios=[1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1,], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("Védelem a fertőzés ellen")

ndx = 0
for csn in csopnevek:
  ax1.plot(dfmerge['Intervallum'].apply(intervallumFormatter), dfmerge[csn], label=csn, marker='o', color = COLORS[ndx])
  ndx += 1
ax1.axhline(0.0,color='magenta',ls='--')
ax1.set(xlabel="Intervallum (hetek)", ylabel="Védelem az oltatlanokhoz képest")
ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
ax1.tick_params(axis='x', rotation=20)
ax1.set_ylim([-150, 350])
ax1.text(2, 320, '18 év alatt nagyon magas a hatásfok', color = 'red')
ax1.text(0, -140, 'A negatív hatásfok az oltatlanok előnyét jelenti', color = 'red')
ax1.legend()


fig.suptitle('Brit COVID adatok\nA vakcinák hatásfoka', fontsize=22)
fig.savefig(BASEDIR + "/anglia-vakcinahatásfok.png")


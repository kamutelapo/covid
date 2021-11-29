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

BASEDIR=os.path.dirname(__file__)
DATADIR=BASEDIR + "/adatok/"

COLORS = [
    '#00FF00', '#00C000', '#0000FF', '#0000C0', '#000080', '#FF0000', '#C00000', '#800000',
]

def intervallumFormatter(x):
    return x + '. hét'

def csoportNevek(dfdata):
    return list(dfdata.columns[1:])

def korcsoportTabla(dfdata, csoportok):
    dfmerge = None

    for csoport in csoportok:
        csopname = csoport
        if csopname == 'Under 18':
            csopname = '18 alatt'
        csopi = dfdata[dfdata['Korcsoport'] == csoport].rename(columns = {'Összes': csopname} )
        csopi = csopi[['Intervallum', csopname]].set_index('Intervallum')
    
        if dfmerge is None:
            dfmerge = csopi
        else:
            dfmerge[csopname] = csopi[csopname]
    
    dfmerge = dfmerge.reset_index()
    return dfmerge

dfcases = pd.read_csv(DATADIR + "data-cases.csv")
dfemergency = pd.read_csv(DATADIR + "data-emergency.csv")
dfdeath = pd.read_csv(DATADIR + "data-death-60.csv")

korcsoportok = dfcases['Korcsoport'].unique()

dfcaseseff = korcsoportTabla(dfcases, korcsoportok)
dfemergencyeff = korcsoportTabla(dfemergency, korcsoportok)
dfdeatheff = korcsoportTabla(dfdeath, korcsoportok)

pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[9,12], constrained_layout=True)

spec = gridspec.GridSpec(ncols=1, nrows=3,
                         width_ratios=[1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1,1,1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("A fertőzöttek életkor szerinti eloszlása")

ndx = 0
for csn in csoportNevek(dfcaseseff):
  ax1.plot(dfcaseseff['Intervallum'].apply(intervallumFormatter), dfcaseseff[csn], label=csn, marker='o', color = COLORS[ndx])
  ndx += 1
ax1.set(xlabel="Intervallum (hetek)", ylabel="Esetek száma")
ax1.tick_params(axis='x', rotation=20)
ax1.legend()

ax2=fig.add_subplot(spec[1], label="2")

ax2.set_title("A kórházi esetek életkor szerinti eloszlása")

ndx = 0
for csn in csoportNevek(dfemergencyeff):
  ax2.plot(dfemergencyeff['Intervallum'].apply(intervallumFormatter), dfemergencyeff[csn], label=csn, marker='o', color = COLORS[ndx])
  ndx += 1
ax2.set(xlabel="Intervallum (hetek)", ylabel="Esetek száma")
ax2.tick_params(axis='x', rotation=20)
ax2.legend()

ax3=fig.add_subplot(spec[2], label="3")

ax3.set_title("A halálesetek életkor szerinti eloszlása")

ndx = 0
for csn in csoportNevek(dfdeatheff):
  ax3.plot(dfdeatheff['Intervallum'].apply(intervallumFormatter), dfdeatheff[csn], label=csn, marker='o', color = COLORS[ndx])
  ndx += 1
ax3.set(xlabel="Intervallum (hetek)", ylabel="Esetek száma")
ax3.tick_params(axis='x', rotation=20)
ax3.legend()

fig.suptitle('Brit COVID adatok\nKorcsoport szerinti eloszlás', fontsize=22)
fig.savefig(BASEDIR + "/anglia-eloszlás.png")


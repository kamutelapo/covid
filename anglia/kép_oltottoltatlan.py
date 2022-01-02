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
    '#00FF00', '#00C000', '#008000', '#4040FF', '#0000D0', '#000080', '#FF6060', '#FF0000', '#800000',
]

def intervallumFormatter(x):
    return x + '.'

def oltottOltatlanTabla(dfdata, csoportok):
    dfmerge = dfdata[dfdata['Korcsoport'].isin(csoportok)]
    dfmerge = dfmerge.groupby('Intervallum').sum()
    dfmerge["Egyszer oltott"] = dfmerge["Egyszer oltott (1-20)"] + dfmerge["Egyszer oltott (21-)"]
    dfmerge = dfmerge.reset_index()

    dfmerge = dfmerge[["Intervallum", "Oltatlan", "Egyszer oltott", "Kétszer oltott"]]
    return dfmerge

dfcases = pd.read_csv(DATADIR + "data-cases.csv")
dfemergency = pd.read_csv(DATADIR + "data-emergency.csv")
dfdeath = pd.read_csv(DATADIR + "data-death-60.csv")

korcsoportok = dfcases['Korcsoport'].unique()

dfcaseseffcs1 = oltottOltatlanTabla(dfcases, korcsoportok[2:])
dfcaseseffcs2 = oltottOltatlanTabla(dfcases, korcsoportok[0:2])
dfemergencyeffcs1 = oltottOltatlanTabla(dfemergency, korcsoportok[2:])
dfemergencyeffcs2 = oltottOltatlanTabla(dfemergency, korcsoportok[0:2])
dfdeatheffcs1 = oltottOltatlanTabla(dfdeath, korcsoportok[2:])
dfdeatheffcs2 = oltottOltatlanTabla(dfdeath, korcsoportok[0:2])

pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[12,12], constrained_layout=True)

spec = gridspec.GridSpec(ncols=2, nrows=3,
                         width_ratios=[1,1], wspace=0.3,
                         hspace=0.38, height_ratios=[1,1,1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("Fertőzöttek 30 év fölött")

iformatter = dfcaseseffcs1['Intervallum'].apply(intervallumFormatter)

ax1.plot(iformatter, dfcaseseffcs1["Egyszer oltott"], label="Egyszer oltott", color = COLORS[2])
ax1.plot(iformatter, dfcaseseffcs1["Egyszer oltott"] + dfcaseseffcs1["Kétszer oltott"], label="Kétszer oltott", color = COLORS[1])
ax1.plot(iformatter, dfcaseseffcs1["Egyszer oltott"] + dfcaseseffcs1["Kétszer oltott"] + dfcaseseffcs1["Oltatlan"], label="Oltatlan", color = COLORS[0])
ax1.fill_between(iformatter, dfcaseseffcs1["Egyszer oltott"] + dfcaseseffcs1["Kétszer oltott"] + dfcaseseffcs1["Oltatlan"], color=COLORS[0])
ax1.fill_between(iformatter, dfcaseseffcs1["Egyszer oltott"] + dfcaseseffcs1["Kétszer oltott"], color=COLORS[1])
ax1.fill_between(iformatter, dfcaseseffcs1["Egyszer oltott"], color=COLORS[2])
ax1.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax1.set_ylim([0, 700000])
ax1.tick_params(axis='x', rotation=45)
ax1.legend(loc = 'upper left')

ax1b=fig.add_subplot(spec[1], label="2")

ax1b.set_title("Fertőzöttek 30 év alatt")

iformatter = dfcaseseffcs2['Intervallum'].apply(intervallumFormatter)

ax1b.plot(iformatter, dfcaseseffcs2["Egyszer oltott"], label="Egyszer oltott", color = COLORS[2])
ax1b.plot(iformatter, dfcaseseffcs2["Egyszer oltott"] + dfcaseseffcs2["Kétszer oltott"], label="Kétszer oltott", color = COLORS[1])
ax1b.plot(iformatter, dfcaseseffcs2["Egyszer oltott"] + dfcaseseffcs2["Kétszer oltott"] + dfcaseseffcs2["Oltatlan"], label="Oltatlan", color = COLORS[0])
ax1b.fill_between(iformatter, dfcaseseffcs2["Egyszer oltott"] + dfcaseseffcs2["Kétszer oltott"] + dfcaseseffcs2["Oltatlan"], color=COLORS[0])
ax1b.fill_between(iformatter, dfcaseseffcs2["Egyszer oltott"] + dfcaseseffcs2["Kétszer oltott"], color=COLORS[1])
ax1b.fill_between(iformatter, dfcaseseffcs2["Egyszer oltott"], color=COLORS[2])
ax1b.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax1b.set_ylim([0, 700000])
ax1b.tick_params(axis='x', rotation=45)
ax1b.legend(loc = 'upper left')

ax2=fig.add_subplot(spec[2], label="3")

ax2.set_title("Kórházi ellátás 30 év fölött")

iformatter = dfemergencyeffcs1['Intervallum'].apply(intervallumFormatter)

ax2.plot(iformatter, dfemergencyeffcs1["Egyszer oltott"], label="Egyszer oltott", color = COLORS[5])
ax2.plot(iformatter, dfemergencyeffcs1["Egyszer oltott"] + dfemergencyeffcs1["Kétszer oltott"], label="Kétszer oltott", color = COLORS[4])
ax2.plot(iformatter, dfemergencyeffcs1["Egyszer oltott"] + dfemergencyeffcs1["Kétszer oltott"] + dfemergencyeffcs1["Oltatlan"], label="Oltatlan", color = COLORS[3])
ax2.fill_between(iformatter, dfemergencyeffcs1["Egyszer oltott"] + dfemergencyeffcs1["Kétszer oltott"] + dfemergencyeffcs1["Oltatlan"], color=COLORS[3])
ax2.fill_between(iformatter, dfemergencyeffcs1["Egyszer oltott"] + dfemergencyeffcs1["Kétszer oltott"], color=COLORS[4])
ax2.fill_between(iformatter, dfemergencyeffcs1["Egyszer oltott"], color=COLORS[5])
ax2.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax2.set_ylim([0, 10000])
ax2.tick_params(axis='x', rotation=45)
ax2.legend(loc = 'upper left')

ax2b=fig.add_subplot(spec[3], label="4")

ax2b.set_title("Kórházi ellátás 30 év alatt")

iformatter = dfemergencyeffcs2['Intervallum'].apply(intervallumFormatter)

ax2b.plot(iformatter, dfemergencyeffcs2["Egyszer oltott"], label="Egyszer oltott", color = COLORS[5])
ax2b.plot(iformatter, dfemergencyeffcs2["Egyszer oltott"] + dfemergencyeffcs2["Kétszer oltott"], label="Kétszer oltott", color = COLORS[4])
ax2b.plot(iformatter, dfemergencyeffcs2["Egyszer oltott"] + dfemergencyeffcs2["Kétszer oltott"] + dfemergencyeffcs2["Oltatlan"], label="Oltatlan", color = COLORS[3])
ax2b.fill_between(iformatter, dfemergencyeffcs2["Egyszer oltott"] + dfemergencyeffcs2["Kétszer oltott"] + dfemergencyeffcs2["Oltatlan"], color=COLORS[3])
ax2b.fill_between(iformatter, dfemergencyeffcs2["Egyszer oltott"] + dfemergencyeffcs2["Kétszer oltott"], color=COLORS[4])
ax2b.fill_between(iformatter, dfemergencyeffcs2["Egyszer oltott"], color=COLORS[5])
ax2b.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax2b.set_ylim([0, 10000])
ax2b.tick_params(axis='x', rotation=45)
ax2b.legend(loc = 'upper left')

ax3=fig.add_subplot(spec[4], label="5")

ax3.set_title("Halál 30 év fölött")

iformatter = dfdeatheffcs1['Intervallum'].apply(intervallumFormatter)

ax3.plot(iformatter, dfdeatheffcs1["Egyszer oltott"], label="Egyszer oltott", color = COLORS[8])
ax3.plot(iformatter, dfdeatheffcs1["Egyszer oltott"] + dfdeatheffcs1["Kétszer oltott"], label="Kétszer oltott", color = COLORS[7])
ax3.plot(iformatter, dfdeatheffcs1["Egyszer oltott"] + dfdeatheffcs1["Kétszer oltott"] + dfdeatheffcs1["Oltatlan"], label="Oltatlan", color = COLORS[6])
ax3.fill_between(iformatter, dfdeatheffcs1["Egyszer oltott"] + dfdeatheffcs1["Kétszer oltott"] + dfdeatheffcs1["Oltatlan"], color=COLORS[6])
ax3.fill_between(iformatter, dfdeatheffcs1["Egyszer oltott"] + dfdeatheffcs1["Kétszer oltott"], color=COLORS[7])
ax3.fill_between(iformatter, dfdeatheffcs1["Egyszer oltott"], color=COLORS[8])
ax3.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax3.set_ylim([0, 5000])
ax3.tick_params(axis='x', rotation=45)
ax3.legend(loc = 'upper left')

ax3b=fig.add_subplot(spec[5], label="6")

ax3b.set_title("Halál 30 év alatt")

iformatter = dfdeatheffcs2['Intervallum'].apply(intervallumFormatter)

ax3b.plot(iformatter, dfdeatheffcs2["Egyszer oltott"], label="Egyszer oltott", color = COLORS[8])
ax3b.plot(iformatter, dfdeatheffcs2["Egyszer oltott"] + dfdeatheffcs2["Kétszer oltott"], label="Kétszer oltott", color = COLORS[7])
ax3b.plot(iformatter, dfdeatheffcs2["Egyszer oltott"] + dfdeatheffcs2["Kétszer oltott"] + dfdeatheffcs2["Oltatlan"], label="Oltatlan", color = COLORS[6])
ax3b.fill_between(iformatter, dfdeatheffcs2["Egyszer oltott"] + dfdeatheffcs2["Kétszer oltott"] + dfdeatheffcs2["Oltatlan"], color=COLORS[6])
ax3b.fill_between(iformatter, dfdeatheffcs2["Egyszer oltott"] + dfdeatheffcs2["Kétszer oltott"], color=COLORS[7])
ax3b.fill_between(iformatter, dfdeatheffcs2["Egyszer oltott"], color=COLORS[8])
ax3b.set(xlabel="Intervallum (hetek)", ylabel="Összes esetek száma")
ax3b.set_ylim([0, 5000])
ax3b.tick_params(axis='x', rotation=45)
ax3b.legend(loc = 'upper left')

fig.suptitle('Brit COVID adatok\nTeljes népességre vonatkozó adatok', fontsize=22)
fig.savefig(BASEDIR + "/anglia-oltottoltatlan.png")


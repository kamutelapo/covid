#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from matplotlib import gridspec
from datetime import timedelta
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates

BASEDIR=os.path.dirname(__file__)

maxdate = pd.to_datetime("2021-12-31")
mindate = pd.to_datetime("2021-01-01")

# KSH többlet

dfksh = pd.read_csv(BASEDIR +"/../adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
dfkshatlag = dfksh[dfksh['A hét záró napja'] < "2020-01-01"]
dfkshatlag = dfkshatlag.groupby('A hét sorszáma').mean().reset_index()
dfkshatlag = dfkshatlag.rename(columns = {'Összesen': 'KSH 5 éves átlag'}, inplace = False)
dfkshatlag = dfkshatlag[["A hét sorszáma", "KSH 5 éves átlag"]]

dfkshmerge = pd.merge(dfksh[['A hét sorszáma', 'A hét kezdő napja', 'Összesen']], dfkshatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkshmerge = dfkshmerge.rename(columns = {'Összesen': 'KSH halálozás', 'A hét kezdő napja': 'Dátum'}, inplace = False)
dfkshmerge['KSH többlet'] = dfkshmerge['KSH halálozás'] - dfkshmerge['KSH 5 éves átlag']

dfksh = dfkshmerge[dfkshmerge['Dátum'] >= mindate]
dfksh = dfksh[dfksh['Dátum'] <= maxdate]


kshtobblet = int(dfksh.sum()['KSH többlet'] + 0.5)


kshmin = int(dfksh.min()['KSH többlet'] - 0.5)
kshtlim1 = int((kshmin - 49) / 50) * 50
kshmax = int(dfksh.max()['KSH többlet'] + 0.5)
kshtlim2 = int((kshmax + 49) / 50) * 50

# rajzolás
    
pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,5])

spec = gridspec.GridSpec(ncols=1, nrows=1,
                         width_ratios=[1], wspace=0.3,
                         hspace=0.40, height_ratios=[1])
spec.update(left=0.06,right=0.95,top=0.92,bottom=0.12,wspace=0.25,hspace=0.50)


formatter = mdates.DateFormatter("%Y-%m-%d")

ax10=fig.add_subplot(spec[0], label="10")
ax10.plot(dfksh['Dátum'], dfksh['KSH többlet'], color='darkviolet')
ax10.set_ylim([kshtlim1,kshtlim2])
ax10.set_title("2021 - KSH többlet halálozás (" + str(kshtobblet) + " fő)", fontweight='bold')
ax10.tick_params(axis='x', rotation=20)
ax10.axhline(0,color='magenta',ls='--')
ax10.fill_between(dfksh['Dátum'], dfksh['KSH többlet'], color="darkviolet")
ax10.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax10.xaxis.set_major_formatter(formatter)

fig.savefig(BASEDIR + "/2021CovidHalálozásiTöbblet.png")

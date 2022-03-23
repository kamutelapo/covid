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

# híradatok

df = pd.read_csv(BASEDIR +"/../adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')
dfroll = df.rolling(7, center=True, min_periods=4).mean()
df['Napi új fertőzött átlag'] = dfroll['Napi új fertőzött']
df['Napi új elhunyt átlag'] = dfroll['Napi új elhunyt']

mindate = pd.to_datetime("2022-01-01")

df2022 = df[df['Dátum'] >= mindate]

# KSH többlet

dfksh = pd.read_csv(BASEDIR +"/../adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
dfkshatlag = dfksh[dfksh['A hét záró napja'] < "2020-01-01"]
dfkshatlag = dfkshatlag.groupby('A hét sorszáma').mean().reset_index()
dfkshatlag = dfkshatlag.rename(columns = {'Összesen': 'KSH 5 éves átlag'}, inplace = False)
dfkshatlag = dfkshatlag[["A hét sorszáma", "KSH 5 éves átlag"]]

maxdateksh = dfksh['A hét kezdő napja'].max()

df2022 = df2022[df2022['Dátum'] <= maxdateksh]

dfkshmerge = pd.merge(dfksh[['A hét sorszáma', 'A hét kezdő napja', 'Összesen']], dfkshatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkshmerge = dfkshmerge.rename(columns = {'Összesen': 'KSH halálozás', 'A hét kezdő napja': 'Dátum'}, inplace = False)
dfkshmerge['KSH többlet'] = dfkshmerge['KSH halálozás'] - dfkshmerge['KSH 5 éves átlag']

dfksh2022 = dfkshmerge[dfkshmerge['Dátum'] >= mindate]
dfksh2022 = dfksh2022[dfksh2022['Dátum'] <= maxdateksh]
dfksh2022 = dfksh2022.sort_values('Dátum')

ksh2022tobblet = int(dfksh2022.sum()['KSH többlet'] + 0.5)

kshmin = int(dfksh2022.min()['KSH többlet'] - 0.5)
kshtlim1 = int((kshmin - 49) / 50) * 50
kshmax = int(dfksh2022.max()['KSH többlet'] + 0.5)
kshtlim2 = int((kshmax + 49) / 50) * 50

# rajzolás
    
pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[6,7])

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         hspace=0.40, height_ratios=[1, 1])
spec.update(left=0.12,right=0.93,top=0.90,bottom=0.08,wspace=0.25,hspace=0.30)


maxuf = int(((df2022.max()['Napi új fertőzött átlag']) + 999) / 1000) * 1000

formatter = mdates.DateFormatter("%Y-%m-%d")
  
ax1=fig.add_subplot(spec[0], label="1")
ax1.plot(df2022['Dátum'], df2022['Napi új fertőzött átlag'], color='orange')
ax1.set_ylim([0,maxuf])
ax1.set_title("2022 - napi új fertőzöttek átlaga", fontweight='bold')
ax1.tick_params(axis='x', rotation=20)
ax1.fill_between(df2022['Dátum'], df2022['Napi új fertőzött átlag'], color="orange")
ax1.xaxis.set_major_formatter(formatter)

ax2=fig.add_subplot(spec[1], label="2")
ax2.plot(dfksh2022['Dátum'], dfksh2022['KSH többlet'], color='darkviolet')
ax2.set_ylim([kshtlim1,kshtlim2])
ax2.set_title("2022 - KSH többlet halálozás (" + str(ksh2022tobblet) + " fő)", fontweight='bold')
ax2.tick_params(axis='x', rotation=20)
ax2.axhline(0,color='magenta',ls='--')
ax2.fill_between(dfksh2022['Dátum'], dfksh2022['KSH többlet'], color="darkviolet")
ax2.add_patch(Rectangle((maxdateksh + timedelta(days = -35), kshtlim1), timedelta(days = 35), kshtlim2 - kshtlim1, facecolor="pink", alpha=0.5, zorder=-10))
ax2.xaxis.set_major_formatter(formatter)

fig.suptitle('Omikron variáns', fontsize=22)
fig.savefig(BASEDIR + "/OmikronVsKsh.png")

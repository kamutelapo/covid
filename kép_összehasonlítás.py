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

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')
dfroll = df.rolling(7, center=True, min_periods=4).mean()
df['Napi új fertőzött átlag'] = dfroll['Napi új fertőzött']
df['Napi új elhunyt átlag'] = dfroll['Napi új elhunyt']

maxdate = df['Dátum'].max()
mindate = pd.to_datetime("2021-08-01")

df2021 = df[df['Dátum'] >= mindate]
df2021 = df2021[df2021['Dátum'] <= maxdate]

maxdate1y = maxdate + timedelta(days = -365)
mindate1y = mindate + timedelta(days = -365)

df2020 = df[df['Dátum'] >= mindate1y]
df2020 = df2020[df2020['Dátum'] <= maxdate1y]
    
pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,8])

spec = gridspec.GridSpec(ncols=2, nrows=3,
                         width_ratios=[1, 1], wspace=0.3,
                         hspace=0.38, height_ratios=[1, 1, 1])
spec.update(left=0.06,right=0.99,top=0.88,bottom=0.08,wspace=0.25,hspace=0.50)


concatfr = pd.concat([df2020, df2021]).max()

maxuf = int(((concatfr['Napi új fertőzött átlag']) + 999) / 1000) * 1000
maxkr = int(((concatfr['Kórházban ápoltak']) + 99) / 100) * 100
maxeh = int(((concatfr['Napi új elhunyt átlag']) + 9) / 10) * 10

ax1=fig.add_subplot(spec[0], label="1")
ax1.plot(df2020['Dátum'], df2020['Napi új fertőzött átlag'], color='orange')
ax1.set_ylim([0,maxuf])
ax1.set_title("2020 - napi új fertőzöttek átlaga")
ax1.tick_params(axis='x', rotation=15)
ax1.fill_between(df2020['Dátum'], df2020['Napi új fertőzött átlag'], color="orange")

ax2=fig.add_subplot(spec[1], label="2")
ax2.plot(df2021['Dátum'], df2021['Napi új fertőzött átlag'], color='orange')
ax2.set_ylim([0,maxuf])
ax2.set_title("2021 - napi új fertőzöttek átlaga")
ax2.tick_params(axis='x', rotation=15)
ax2.fill_between(df2021['Dátum'], df2021['Napi új fertőzött átlag'], color="orange")

ax3=fig.add_subplot(spec[2], label="3")
ax3.plot(df2020['Dátum'], df2020['Kórházban ápoltak'], color='blue')
ax3.set_ylim([0,maxkr])
ax3.set_title("2020 - kórházban ápoltak")
ax3.tick_params(axis='x', rotation=15)
ax3.fill_between(df2020['Dátum'], df2020['Kórházban ápoltak'], color="blue")

ax4=fig.add_subplot(spec[3], label="4")
ax4.plot(df2021['Dátum'], df2021['Kórházban ápoltak'], color='blue')
ax4.set_ylim([0,maxkr])
ax4.set_title("2021 - kórházban ápoltak")
ax4.tick_params(axis='x', rotation=15)
ax4.fill_between(df2021['Dátum'], df2021['Kórházban ápoltak'], color="blue")

ax5=fig.add_subplot(spec[4], label="5")
ax5.plot(df2020['Dátum'], df2020['Napi új elhunyt átlag'], color='red')
ax5.set_ylim([0,maxeh])
ax5.set_title("2020 - elhunytak átlaga")
ax5.tick_params(axis='x', rotation=15)
ax5.fill_between(df2020['Dátum'], df2020['Napi új elhunyt átlag'], color="red")

ax6=fig.add_subplot(spec[5], label="6")
ax6.plot(df2021['Dátum'], df2021['Napi új elhunyt átlag'], color='red')
ax6.set_ylim([0,maxeh])
ax6.set_title("2021 - elhunytak átlaga")
ax6.tick_params(axis='x', rotation=15)
ax6.fill_between(df2021['Dátum'], df2021['Napi új elhunyt átlag'], color="red")

fig.suptitle('COVID járvány összehasonlítás', fontsize=22)
fig.savefig(BASEDIR + "/képek/CovidÖsszehasonlítás.png")

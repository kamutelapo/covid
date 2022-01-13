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

# KSH többlet

dfksh = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kezdő napja', 'A hét záró napja'], delimiter=';')
dfkshatlag = dfksh[dfksh['A hét záró napja'] < "2020-01-01"]
dfkshatlag = dfkshatlag.groupby('A hét sorszáma').mean().reset_index()
dfkshatlag = dfkshatlag.rename(columns = {'Összesen': 'KSH 5 éves átlag'}, inplace = False)
dfkshatlag = dfkshatlag[["A hét sorszáma", "KSH 5 éves átlag"]]

maxdateksh = dfksh['A hét kezdő napja'].max()
maxdateksh1y = maxdateksh + timedelta(days = -360)

dfkshmerge = pd.merge(dfksh[['A hét sorszáma', 'A hét kezdő napja', 'Összesen']], dfkshatlag, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkshmerge = dfkshmerge.rename(columns = {'Összesen': 'KSH halálozás', 'A hét kezdő napja': 'Dátum'}, inplace = False)
dfkshmerge['KSH többlet'] = dfkshmerge['KSH halálozás'] - dfkshmerge['KSH 5 éves átlag']

dfksh2020 = dfkshmerge[dfkshmerge['Dátum'] >= mindate1y]
dfksh2020 = dfksh2020[dfksh2020['Dátum'] <= maxdateksh1y]

dfksh2021 = dfkshmerge[dfkshmerge['Dátum'] >= mindate]
dfksh2021 = dfksh2021[dfksh2021['Dátum'] <= maxdateksh]

ksh2020tobblet = int(dfksh2020.sum()['KSH többlet'] + 0.5)
ksh2021tobblet = int(dfksh2021.sum()['KSH többlet'] + 0.5)

concatksh = pd.concat([dfksh2020, dfksh2021])
kshmin = int(concatksh.min()['KSH többlet'] - 0.5)
kshtlim1 = int((kshmin - 49) / 50) * 50
kshmax = int(concatksh.max()['KSH többlet'] + 0.5)
kshtlim2 = int((kshmax + 49) / 50) * 50

# rajzolás
    
pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,13])

spec = gridspec.GridSpec(ncols=2, nrows=5,
                         width_ratios=[1, 1], wspace=0.3,
                         hspace=0.40, height_ratios=[1, 1, 1, 1, 1])
spec.update(left=0.06,right=0.95,top=0.92,bottom=0.08,wspace=0.25,hspace=0.50)


concatfr = pd.concat([df2020, df2021]).max()

maxuf = int(((concatfr['Napi új fertőzött átlag']) + 999) / 1000) * 1000
maxkr = int(((concatfr['Kórházban ápoltak']) + 99) / 100) * 100
maxeh = int(((concatfr['Napi új elhunyt átlag']) + 9) / 10) * 10
maxlg = int(((concatfr['Lélegeztetettek']) + 19) / 20) * 20

formatter = mdates.DateFormatter("%Y-%m-%d")

ax1=fig.add_subplot(spec[0], label="1")
ax1.plot(df2020['Dátum'], df2020['Napi új fertőzött átlag'], color='orange')
ax1.set_ylim([0,maxuf])
ax1.set_title("2020 - napi új fertőzöttek átlaga", fontweight='bold')
ax1.tick_params(axis='x', rotation=20)
ax1.fill_between(df2020['Dátum'], df2020['Napi új fertőzött átlag'], color="orange")
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_major_formatter(formatter)
    
ax2=fig.add_subplot(spec[1], label="2")
ax2.plot(df2021['Dátum'], df2021['Napi új fertőzött átlag'], color='orange')
ax2.set_ylim([0,maxuf])
ax2.set_title("2021 - napi új fertőzöttek átlaga", fontweight='bold')
ax2.tick_params(axis='x', rotation=20)
ax2.fill_between(df2021['Dátum'], df2021['Napi új fertőzött átlag'], color="orange")
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax2.xaxis.set_major_formatter(formatter)

ax3=fig.add_subplot(spec[2], label="3")
ax3.plot(df2020['Dátum'], df2020['Kórházban ápoltak'], color='blue')
ax3.set_ylim([0,maxkr])
ax3.set_title("2020 - kórházban ápoltak", fontweight='bold')
ax3.tick_params(axis='x', rotation=20)
ax3.fill_between(df2020['Dátum'], df2020['Kórházban ápoltak'], color="blue")
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax3.xaxis.set_major_formatter(formatter)

ax4=fig.add_subplot(spec[3], label="4")
ax4.plot(df2021['Dátum'], df2021['Kórházban ápoltak'], color='blue')
ax4.set_ylim([0,maxkr])
ax4.set_title("2021 - kórházban ápoltak", fontweight='bold')
ax4.tick_params(axis='x', rotation=20)
ax4.fill_between(df2021['Dátum'], df2021['Kórházban ápoltak'], color="blue")
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax4.xaxis.set_major_formatter(formatter)

ax5=fig.add_subplot(spec[4], label="5")
ax5.plot(df2020['Dátum'], df2020['Napi új elhunyt átlag'], color='red')
ax5.set_ylim([0,maxeh])
ax5.set_title("2020 - elhunytak átlaga", fontweight='bold')
ax5.tick_params(axis='x', rotation=20)
ax5.fill_between(df2020['Dátum'], df2020['Napi új elhunyt átlag'], color="red")
ax5.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax5.xaxis.set_major_formatter(formatter)

ax6=fig.add_subplot(spec[5], label="6")
ax6.plot(df2021['Dátum'], df2021['Napi új elhunyt átlag'], color='red')
ax6.set_ylim([0,maxeh])
ax6.set_title("2021 - elhunytak átlaga", fontweight='bold')
ax6.tick_params(axis='x', rotation=20)
ax6.fill_between(df2021['Dátum'], df2021['Napi új elhunyt átlag'], color="red")
ax6.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax6.xaxis.set_major_formatter(formatter)

ax7=fig.add_subplot(spec[6], label="7")
ax7.plot(df2020['Dátum'], df2020['Lélegeztetettek'], color='green')
ax7.set_ylim([0,maxlg])
ax7.set_title("2020 - lélegeztetettek", fontweight='bold')
ax7.tick_params(axis='x', rotation=20)
ax7.fill_between(df2020['Dátum'], df2020['Lélegeztetettek'], color="green")
ax7.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax7.xaxis.set_major_formatter(formatter)

ax8=fig.add_subplot(spec[7], label="8")
ax8.plot(df2021['Dátum'], df2021['Lélegeztetettek'], color='green')
ax8.set_ylim([0,maxlg])
ax8.set_title("2021 - lélegeztetettek", fontweight='bold')
ax8.tick_params(axis='x', rotation=20)
ax8.fill_between(df2021['Dátum'], df2021['Lélegeztetettek'], color="green")
ax8.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax8.xaxis.set_major_formatter(formatter)

ax9=fig.add_subplot(spec[8], label="9")
ax9.plot(dfksh2020['Dátum'], dfksh2020['KSH többlet'], color='darkviolet')
ax9.set_ylim([kshtlim1,kshtlim2])
ax9.set_title("2020 - KSH többlet halálozás (" + str(ksh2020tobblet) + " fő)", fontweight='bold')
ax9.tick_params(axis='x', rotation=20)
ax9.axhline(0,color='magenta',ls='--')
ax9.fill_between(dfksh2020['Dátum'], dfksh2020['KSH többlet'], color="darkviolet")
ax9.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax9.xaxis.set_major_formatter(formatter)

ax10=fig.add_subplot(spec[9], label="10")
ax10.plot(dfksh2021['Dátum'], dfksh2021['KSH többlet'], color='darkviolet')
ax10.set_ylim([kshtlim1,kshtlim2])
ax10.set_title("2021 - KSH többlet halálozás (" + str(ksh2021tobblet) + " fő)", fontweight='bold')
ax10.tick_params(axis='x', rotation=20)
ax10.axhline(0,color='magenta',ls='--')
ax10.fill_between(dfksh2021['Dátum'], dfksh2021['KSH többlet'], color="darkviolet")
ax10.add_patch(Rectangle((maxdateksh + timedelta(days = -35), kshtlim1), timedelta(days = 35), kshtlim2 - kshtlim1, facecolor="pink", alpha=0.5, zorder=-10))
ax10.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax10.xaxis.set_major_formatter(formatter)

fig.suptitle('COVID járvány összehasonlítás', fontsize=22)
fig.savefig(BASEDIR + "/képek/CovidÖsszehasonlítás.png")

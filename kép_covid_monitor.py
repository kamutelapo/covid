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

MASODIK_HULLAM_START = '2020-10-05'
MASODIK_HULLAM_END = '2021-01-26'

HARMADIK_HULLAM_START = '2021-01-27'
HARMADIK_HULLAM_END = '2021-05-20'

NEGYEDIK_HULLAM_START = '2021-06-21'
NEGYEDIK_HULLAM_END = '2021-10-15'

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')

dfeh = pd.read_csv(BASEDIR +"/adatok/elhunytak_datummal.csv", parse_dates=['Dátum']).sort_values(by = ['Dátum']).reset_index()

dfeh50 = dfeh.copy()
dfeh50 = dfeh50[dfeh50['Kor'] <= 50]
dfeh50 = dfeh50[dfeh50['Dátum'] >= '2020-04-08']

dfehavg = dfeh["Kor"].rolling(50).mean().reset_index()
dfehavg["Dátum"] = dfeh["Dátum"]

elhunyt50 = dfeh50.groupby('Dátum').count().reset_index()
elhunyt50 = elhunyt50.rename(columns = {'Sorszám': 'Napi új elhunyt 50 alatt'}, inplace = False)
elhunyt50 = elhunyt50[['Dátum', 'Napi új elhunyt 50 alatt']]

dfeh = dfehavg.groupby("Dátum").last().reset_index()
ddf = pd.DataFrame(pd.date_range(start = dfeh['Dátum'].min(), end = dfeh['Dátum'].max()), columns=['Dátum'])
dfeh = pd.merge(dfeh, ddf, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum').reset_index()
dfeh['Kor'] = dfeh['Kor'].interpolate(method='linear')

date_range_4h = pd.DataFrame({'Dátum': pd.date_range(start=NEGYEDIK_HULLAM_START, end=NEGYEDIK_HULLAM_END)})
df = pd.merge(df, date_range_4h, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum')
df = pd.merge(df, elhunyt50, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum')
dfeh = pd.merge(df, dfeh, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum')

df["Napi új elhunyt 50 alatt"] = df["Napi új elhunyt 50 alatt"].fillna(0)

df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfhd = df.rolling(7).mean().shift(-6)

elozoertekhd = dfhd.iloc[:-7]['Napi új fertőzött']
elsonanhd = pd.DataFrame([[np.NaN]] * 7);
elozoertekhd = pd.concat([elsonanhd, elozoertekhd], ignore_index=True)
elozoertekhd.columns = ['Előző fertőzött átlag']

dfhd['Előző fertőzött átlag'] = elozoertekhd['Előző fertőzött átlag']
dfhd = dfhd.rename(columns = {'Napi új fertőzött': 'Heti új fertőzöttek átlaga', 'Napi új elhunyt': 'Napi új elhunytak átlaga', 
                              'Napi új elhunyt 50 alatt': 'Napi új elhunytak átlaga 50 alatt'}, inplace = False)
dfhd['Terjedés'] = dfhd['Heti új fertőzöttek átlaga'] / dfhd['Előző fertőzött átlag']
dfhd['Dátum'] = df['Dátum']

dfhd['Lélegeztetettek'] = df['Lélegeztetettek']
dfhd['Kórházban ápoltak'] = df['Kórházban ápoltak']

dfheti = (df.groupby('Hét kezdet', as_index=False).mean())
dfheti = dfheti.rename(columns = {'Napi új fertőzött': "Heti új fertőzöttek átlaga", "Napi új elhunyt": "Napi új elhunytak átlaga", 'Hét kezdet': 'Dátum'}, inplace = False)

elsonan = pd.DataFrame([[np.NaN]]);
elozoertek = dfheti.iloc[:-1]['Heti új fertőzöttek átlaga']
elozoertek = pd.concat([elsonan, elozoertek], ignore_index=True)
elozoertek.columns = ['Előző fertőzött átlag']

dfheti['Előző fertőzött átlag'] = elozoertek['Előző fertőzött átlag']
dfheti['Terjedés'] = dfheti['Heti új fertőzöttek átlaga'] / dfheti['Előző fertőzött átlag']

dfheti = dfheti[['Dátum', "Heti új fertőzöttek átlaga", "Napi új elhunytak átlaga", 'Előző fertőzött átlag', 'Terjedés']]

# 2. hullám

df2 = dfheti[dfheti['Dátum'] >= MASODIK_HULLAM_START]
df2 = df2[df2['Dátum'] < MASODIK_HULLAM_END]
df2hd = dfhd[dfhd['Dátum'] >= MASODIK_HULLAM_START]
df2hd = df2hd[df2hd['Dátum'] < MASODIK_HULLAM_END]
df2eh = dfeh[dfeh['Dátum'] >= MASODIK_HULLAM_START]
df2eh = df2eh[df2eh['Dátum'] < MASODIK_HULLAM_END]

# 3. hullám

df3 = dfheti[dfheti['Dátum'] >= HARMADIK_HULLAM_START]
df3 = df3[df3['Dátum'] < HARMADIK_HULLAM_END]
df3hd = dfhd[dfhd['Dátum'] >= HARMADIK_HULLAM_START]
df3hd = df3hd[df3hd['Dátum'] < HARMADIK_HULLAM_END]
df3eh = dfeh[dfeh['Dátum'] >= HARMADIK_HULLAM_START]
df3eh = df3eh[df3eh['Dátum'] < HARMADIK_HULLAM_END]

# 4. hullám

df4 = dfheti[dfheti['Dátum'] >= NEGYEDIK_HULLAM_START]
df4 = df4[df4['Dátum'] < NEGYEDIK_HULLAM_END]
df4hd = dfhd[dfhd['Dátum'] >= NEGYEDIK_HULLAM_START]
df4hd = df4hd[df4hd['Dátum'] < NEGYEDIK_HULLAM_END]
df4eh = dfeh[dfeh['Dátum'] >= NEGYEDIK_HULLAM_START]
df4eh = df4eh[df4eh['Dátum'] < NEGYEDIK_HULLAM_END]

pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,9.5])

spec = gridspec.GridSpec(ncols=3, nrows=6,
                         width_ratios=[1, 1, 1], wspace=0.3,
                         hspace=0.38, height_ratios=[1.3, 1, 1, 1, 1, 0.6])
spec.update(left=0.06,right=0.99,top=0.91,bottom=0.01,wspace=0.25,hspace=0.35)

ax=fig.add_subplot(spec[0], label="1")
ax.bar(df2['Dátum'], df2['Terjedés'], width=2.0)
ax.set_ylim([0,3.0])
ax.xaxis.set_visible(False)
ax.set_title("A 2. hullám heti dinamikája")
ax.axhline(1.0,color='magenta',ls='--')

ax2=fig.add_subplot(spec[0], label="2", frame_on=False)
ax2.plot(df2hd['Dátum'], df2hd['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o', markevery=(0,7))
ax2.set_ylim([0,10000])
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

ax3=fig.add_subplot(spec[1], label="3")
ax3.bar(df3['Dátum'], df3['Terjedés'], width=2.0)
ax3.set_ylim([0,3.0])
ax3.xaxis.set_visible(False)
ax3.set_title("A 3. hullám heti dinamikája")
ax3.axhline(1.0,color='magenta',ls='--')

ax4=fig.add_subplot(spec[1], label="4", frame_on=False)
ax4.plot(df3hd['Dátum'], df3hd['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o', markevery=(0,7))
ax4.set_ylim([0,10000])
ax4.xaxis.set_visible(False)
ax4.yaxis.set_visible(False)

ax5=fig.add_subplot(spec[2], label="5")
ax5.bar(df4['Dátum'], df4['Terjedés'], width=2.0)
ax5.set_ylim([0,3.0])
ax5.set_xlim([df4['Dátum'].min() + pd.Timedelta("-5 days"), df4['Dátum'].max()])
ax5.xaxis.set_visible(False)
ax5.set_title("A 4. hullám heti dinamikája")
ax5.axhline(1.0,color='magenta',ls='--')

ax6=fig.add_subplot(spec[2], label="6", frame_on=False)
ax6.plot(df4hd['Dátum'], df4hd['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o', markevery=(0,7))
ax6.set_ylim([0,100])
ax6.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax6.xaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax7=fig.add_subplot(spec[3], label="7")
ax7.plot(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga'], color="red")
ax7.set_ylim([0,300])
ax7.xaxis.set_visible(False)
ax7.set_title("2. hullám, elhunytak & 50 alatt")
ax7.fill_between(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga'], color="red")

ax7b=fig.add_subplot(spec[3], label="7b", frame_on=False)
ax7b.plot(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")
ax7b.set_ylim([0,300])
ax7b.xaxis.set_visible(False)
ax7b.yaxis.set_visible(False)
ax7b.fill_between(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")

ax8=fig.add_subplot(spec[4], label="8")
ax8.plot(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga'], color="red")
ax8.set_ylim([0,300])
ax8.xaxis.set_visible(False)
ax8.set_title("3. hullám, elhunytak & 50 alatt")
ax8.fill_between(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga'], color="red")

ax8b=fig.add_subplot(spec[4], label="8b", frame_on=False)
ax8b.plot(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")
ax8b.set_ylim([0,300])
ax8b.xaxis.set_visible(False)
ax8b.yaxis.set_visible(False)
ax8b.fill_between(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")

ax9=fig.add_subplot(spec[5], label="9")
ax9.plot(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga'], color="red")
ax9.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax9.set_ylim([0,300])
ax9.xaxis.set_visible(False)
ax9.set_title("4. hullám, elhunytak & 50 alatt")
ax9.fill_between(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga'], color="red")

ax9b=fig.add_subplot(spec[5], label="9b", frame_on=False)
ax9b.plot(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")
ax9b.set_ylim([0,300])
ax9b.xaxis.set_visible(False)
ax9b.yaxis.set_visible(False)
ax9b.fill_between(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga 50 alatt'], color="cyan")

ax10=fig.add_subplot(spec[6], label="10")
ax10.plot(df2hd['Dátum'], df2hd['Lélegeztetettek'], color="green")
ax10.set_ylim([0,1600])
ax10.xaxis.set_visible(False)
ax10.set_title("2. hullám, lélegeztetettek")
ax10.fill_between(df2hd['Dátum'], df2hd['Lélegeztetettek'], color="green")

ax11=fig.add_subplot(spec[7], label="11")
ax11.plot(df3hd['Dátum'], df3hd['Lélegeztetettek'], color="green")
ax11.set_ylim([0,1600])
ax11.xaxis.set_visible(False)
ax11.set_title("3. hullám, lélegeztetettek")
ax11.fill_between(df3hd['Dátum'], df3hd['Lélegeztetettek'], color="green")

ax12=fig.add_subplot(spec[8], label="12")
ax12.plot(df4hd['Dátum'], df4hd['Lélegeztetettek'], color="green")
ax12.set_ylim([0,1600])
ax12.xaxis.set_visible(False)
ax12.set_title("4. hullám, lélegeztetettek")
ax12.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax12.fill_between(df4hd['Dátum'], df4hd['Lélegeztetettek'], color="green")

ax13=fig.add_subplot(spec[9], label="13")
ax13.plot(df2hd['Dátum'], df2hd['Kórházban ápoltak'], color="blue")
ax13.set_ylim([0,13000])
ax13.xaxis.set_visible(False)
ax13.set_title("2. hullám, kórházban ápoltak")
ax13.fill_between(df2hd['Dátum'], df2hd['Kórházban ápoltak'], color="blue")

ax14=fig.add_subplot(spec[10], label="14")
ax14.plot(df3hd['Dátum'], df3hd['Kórházban ápoltak'], color="blue")
ax14.set_ylim([0,13000])
ax14.xaxis.set_visible(False)
ax14.set_title("3. hullám, kórházban ápoltak")
ax14.fill_between(df3hd['Dátum'], df3hd['Kórházban ápoltak'], color="blue")

ax15=fig.add_subplot(spec[11], label="15")
ax15.plot(df4hd['Dátum'], df4hd['Kórházban ápoltak'], color="blue")
ax15.set_ylim([0,13000])
ax15.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax15.xaxis.set_visible(False)
ax15.set_title("4. hullám, kórházban ápoltak")
ax15.fill_between(df4hd['Dátum'], df4hd['Kórházban ápoltak'], color="blue")

ax16=fig.add_subplot(spec[12], label="16")
ax16.plot(df2eh['Dátum'], df2eh['Kor'], color="darkcyan")
ax16.set_ylim([65,80])
ax16.xaxis.set_visible(False)
ax16.set_title("2. hullám, elhunytak életkora")

ax17=fig.add_subplot(spec[13], label="17")
ax17.plot(df3eh['Dátum'], df3eh['Kor'], color="darkcyan")
ax17.set_ylim([65,80])
ax17.xaxis.set_visible(False)
ax17.set_title("3. hullám, elhunytak életkora")

ax18=fig.add_subplot(spec[14], label="18")
ax18.plot(df4eh['Dátum'], df4eh['Kor'], color="darkcyan")
ax18.set_xlim([df4eh['Dátum'].min() + pd.Timedelta("-5 days"), df4eh['Dátum'].max()])
ax18.set_ylim([65,80])
ax18.xaxis.set_visible(False)
ax18.set_title("4. hullám, elhunytak életkora")

#pd.set_option("display.max_rows", None)
#print (df4eh)

ax19=fig.add_subplot(spec[5,:])
ax19.xaxis.set_visible(False)
ax19.yaxis.set_visible(False)
ax19.set_title("Adatok szöveges kiértékelése", color = "indigo")
ax19.text(x=0.01, y=0.05, s="Szöveges kiértékelés itt...\n\n\n", color = "indigo")
fig.suptitle('COVID járvány monitor', fontsize=22)
fig.savefig(BASEDIR + "/képek/CovidMonitor.png")

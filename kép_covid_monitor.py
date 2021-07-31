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

NEGYEDIK_HULLAM_START = '2021-06-21'
NEGYEDIK_HULLAM_END = '2021-09-08'

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')
df['Kórházban ápoltak'] = df['Kórházban ápoltak'].interpolate(method='linear')

date_range_4h = pd.DataFrame({'Dátum': pd.date_range(start=NEGYEDIK_HULLAM_START, end=NEGYEDIK_HULLAM_END)})
df = pd.merge(df, date_range_4h, left_on = 'Dátum', right_on = 'Dátum', how="outer").sort_values('Dátum')

df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfhd = df.rolling(7).mean().shift(-6)

elozoertekhd = dfhd.iloc[:-7]['Napi új fertőzött']
elsonanhd = pd.DataFrame([[np.NaN]] * 7);
elozoertekhd = pd.concat([elsonanhd, elozoertekhd], ignore_index=True)
elozoertekhd.columns = ['Előző fertőzött átlag']

dfhd['Előző fertőzött átlag'] = elozoertekhd['Előző fertőzött átlag']
dfhd = dfhd.rename(columns = {'Napi új fertőzött': 'Heti új fertőzöttek átlaga', 'Napi új elhunyt': 'Napi új elhunytak átlaga'}, inplace = False)
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

df2 = dfheti[dfheti['Dátum'] >= "2020-10-05"]
df2 = df2[df2['Dátum'] < "2020-12-29"]
df2hd = dfhd[dfhd['Dátum'] >= "2020-10-05"]
df2hd = df2hd[df2hd['Dátum'] < "2020-12-29"]

# 3. hullám

df3 = dfheti[dfheti['Dátum'] >= "2021-01-25"]
df3 = df3[df3['Dátum'] < "2021-04-20"]
df3hd = dfhd[dfhd['Dátum'] >= "2021-01-25"]
df3hd = df3hd[df3hd['Dátum'] < "2021-04-20"]

# 4. hullám

df4 = dfheti[dfheti['Dátum'] >= NEGYEDIK_HULLAM_START]
df4 = df4[df4['Dátum'] < NEGYEDIK_HULLAM_END]
df4hd = dfhd[dfhd['Dátum'] >= NEGYEDIK_HULLAM_START]
df4hd = df4hd[df4hd['Dátum'] < NEGYEDIK_HULLAM_END]

pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[10,8.5])

spec = gridspec.GridSpec(ncols=3, nrows=4,
                         width_ratios=[1, 1, 1], wspace=0.3,
                         hspace=0.4, height_ratios=[1.3, 1, 1, 1])
spec.update(left=0.06,right=0.99,top=0.89,bottom=0.1,wspace=0.25,hspace=0.35)

ax=fig.add_subplot(spec[0], label="1")
ax.bar(df2['Dátum'], df2['Terjedés'], width=2.0)
ax.set_ylim([0,3.0])
ax.xaxis.set_visible(False)
ax.set_title("A 2. hullám heti dinamikája")
ax.axhline(1.0,color='magenta',ls='--')

ax2=fig.add_subplot(spec[0], label="2", frame_on=False)
ax2.plot(df2hd['Dátum'], df2hd['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o', markevery=(0,7))
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
ax6.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax6.xaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax7=fig.add_subplot(spec[3], label="7")
ax7.plot(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga'], color="red")
ax7.set_ylim([0,300])
ax7.xaxis.set_visible(False)
ax7.set_title("2. hullám, elhunytak")
ax7.fill_between(df2hd['Dátum'], df2hd['Napi új elhunytak átlaga'], color="red")

ax8=fig.add_subplot(spec[4], label="8")
ax8.plot(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga'], color="red")
ax8.set_ylim([0,300])
ax8.xaxis.set_visible(False)
ax8.set_title("3. hullám, elhunytak")
ax8.fill_between(df3hd['Dátum'], df3hd['Napi új elhunytak átlaga'], color="red")

ax9=fig.add_subplot(spec[5], label="9")
ax9.plot(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga'], color="red")
ax9.set_xlim([df4hd['Dátum'].min() + pd.Timedelta("-5 days"), df4hd['Dátum'].max()])
ax9.set_ylim([0,300])
ax9.xaxis.set_visible(False)
ax9.set_title("4. hullám, elhunytak")
ax9.fill_between(df4hd['Dátum'], df4hd['Napi új elhunytak átlaga'], color="red")

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

fig.text(.01, .02, "")

fig.suptitle('COVID járvány monitor', fontsize=26)
fig.savefig(BASEDIR + "/képek/CovidMonitor.png")

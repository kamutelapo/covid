#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/covidadatok.csv", parse_dates=['Dátum'])
df['Hét kezdet'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)

dfheti = (df.groupby('Hét kezdet', as_index=False).mean())
dfheti = dfheti.rename(columns = {'Napi új fertőzött': "Heti új fertőzöttek átlaga", 'Hét kezdet': 'Dátum'}, inplace = False)

elsonan = pd.DataFrame([[np.NaN]]);
elozoertek = dfheti.iloc[:-1]['Heti új fertőzöttek átlaga']
elozoertek = pd.concat([elsonan, elozoertek], ignore_index=True)
elozoertek.columns = ['Előző fertőzött átlag']

dfheti['Előző fertőzött átlag'] = elozoertek['Előző fertőzött átlag']
dfheti['Terjedés'] = dfheti['Heti új fertőzöttek átlaga'] / dfheti['Előző fertőzött átlag']

dfheti = dfheti[['Dátum', "Heti új fertőzöttek átlaga", 'Előző fertőzött átlag', 'Terjedés']]

df2 = dfheti[dfheti['Dátum'] >= "2020-09-29"]
df2 = df2[df2['Dátum'] < "2020-12-20"]

df3 = dfheti[dfheti['Dátum'] >= "2021-01-25"]
df3 = df3[df3['Dátum'] < "2021-04-12"]

pd.plotting.register_matplotlib_converters()

x_values1=[1,2,3,4,5]
y_values1=[1,2,2,4,1]

x_values2=[-1000,-800,-600,-400,-200]
y_values2=[10,20,39,40,50]

x_values3=[150,200,250,300,350]
y_values3=[10,20,30,40,50]


fig=plt.figure(figsize=[8,5])

ax=fig.add_subplot(121, label="1")
ax.bar(df2['Dátum'], df2['Terjedés'], width=2.0)
ax.set_ylim([0,3.0])
ax.xaxis.set_visible(False)
ax.set_title("A 2. hullám heti dinamikája")
ax.axhline(1.0,color='magenta',ls='--')

ax2=fig.add_subplot(121, label="2", frame_on=False)
ax2.plot(df2['Dátum'], df2['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o')
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

ax3=fig.add_subplot(122, label="3")
ax3.bar(df3['Dátum'], df3['Terjedés'], width=2.0)
ax3.set_ylim([0,3.0])
ax3.xaxis.set_visible(False)
ax3.set_title("A 3. hullám heti dinamikája")
ax3.axhline(1.0,color='magenta',ls='--')

ax4=fig.add_subplot(122, label="4", frame_on=False)
ax4.plot(df3['Dátum'], df3['Előző fertőzött átlag'], color="orange", linewidth=2.0, marker='o')
ax4.xaxis.set_visible(False)
ax4.yaxis.set_visible(False)

fig.savefig(BASEDIR + "/képek/VírusTerjedésCsúcsok.png", bbox_inches = "tight")

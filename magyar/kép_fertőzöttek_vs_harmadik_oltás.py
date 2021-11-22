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

BASEDIR=os.path.dirname(__file__)


df = pd.read_csv(BASEDIR +"/újfertőzések.csv", parse_dates=['Dátum'])
df["Oltottak aránya"] =100 * df['Legalább 1 oltással rendelkezők száma'] / df['Regisztrált fertőzöttek száma']

dfhir = pd.read_csv(BASEDIR +"/../adatok/hiradatok.csv", parse_dates=['Dátum'])

df = pd.merge(df, dfhir, left_on = 'Dátum', right_on = 'Dátum', how="left")

pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[6,6])

spec = gridspec.GridSpec(ncols=1, nrows=2,
                         width_ratios=[1], wspace=0.3,
                         hspace=0.40, height_ratios=[1, 1])
spec.update(left=0.06,right=0.95,top=0.92,bottom=0.08,wspace=0.25,hspace=0.50)

ax1=fig.add_subplot(spec[0], label="1")
ax1.set_title("Megfertőződött oltottak aránya és a harmadik oltások")
ax1.plot(df['Dátum'], df['Oltottak aránya'], color='orange')
ax1.set_ylim([0,100])
ax1.tick_params(axis='x', rotation=20)
ax1.set_ylabel("Oltottak aránya", color="orange")

ax2=ax1.twinx()
ax2.plot(df['Dátum'], df['Háromszor oltottak'], color='blue')
ax2.set_ylim([0,1300000])
ax2.set_ylabel("Háromszor oltottak", color="blue")

korr = df['Oltottak aránya'].corr(df['Háromszor oltottak'])

dfkorr = pd.DataFrame(data={'Név': ['Erős összefüggés', 'Mérsékelt összefüggés', 'Gyenge összefüggés', 'Harmadik oltások',
                                    'Gyenge ellentétes összefüggés', 'Mérsékelt ellentétes összefüggés', 'Erős ellentétes összefüggés'], 
                            'Korreláció': [0.75, 0.5, 0.25, korr, -0.27, -0.5, -0.75],
                            'Szín': ['blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue']})
dfkorr.sort_values('Korreláció',inplace=True)

korrstr = str(int (korr * 100) / 100)

ax3=fig.add_subplot(spec[1], label="2")
ax3.set_title("Korreláció a görbék között (" + korrstr + ", nincs összefüggés)")

ax3.barh(dfkorr['Név'], dfkorr['Korreláció'], color = dfkorr['Szín'])


fig.savefig(BASEDIR + "/FertőzésVsHarmadikOltás.png", bbox_inches = "tight")
    
plt.clf()

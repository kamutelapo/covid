#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import pandas as pd
from matplotlib import gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np
import mpl_toolkits.axisartist as AA

BASEDIR=os.path.dirname(__file__)

def smallerThan5Random(c):
    if c == '<5':
        return str(np.random.randint(4)+1)
    return c

# új esetek tábla

dfuj = pd.read_csv(BASEDIR + "/cases-among-vaccinated.csv")
dfuj = dfuj.fillna(0)

COLUMN_LIST = ['positive_1_6_days_after_1st_dose', 'positive_7_13_days_after_1st_dose', 'positive_14_20_days_after_1st_dose', 'positive_above_20_days_after_1st_dose', 'positive_1_6_days_after_2nd_dose',
               'positive_7_13_days_after_2nd_dose', 'positive_14_30_days_after_2nd_dose', 'positive_31_90_days_after_2nd_dose', 'positive_above_3_month_after_2nd_before_3rd_dose', 'positive_1_6_days_after_3rd_dose',
               'positive_7_13_days_after_3rd_dose', 'positive_14_30_days_after_3rd_dose', 'positive_above_90_days_after_3rd_dose', 'Sum_positive_without_vaccination']

for column in COLUMN_LIST:
    dfuj[column] = dfuj.apply(lambda row: smallerThan5Random(row[column]), axis=1)

for column in COLUMN_LIST:
    dfuj[column] = dfuj[column].astype(float)
    dfuj[column] = dfuj[column].astype(int)
    
dfuj['Oltott'] = dfuj['positive_1_6_days_after_1st_dose'] + dfuj['positive_7_13_days_after_1st_dose'] + dfuj['positive_14_20_days_after_1st_dose'] + dfuj['positive_above_20_days_after_1st_dose'] + \
                 dfuj['positive_1_6_days_after_2nd_dose'] + dfuj['positive_7_13_days_after_2nd_dose'] + dfuj['positive_14_30_days_after_2nd_dose'] + dfuj['positive_31_90_days_after_2nd_dose'] + \
                 dfuj['positive_above_3_month_after_2nd_before_3rd_dose'] + dfuj['positive_1_6_days_after_3rd_dose'] + dfuj['positive_7_13_days_after_3rd_dose'] + dfuj['positive_14_30_days_after_3rd_dose'] + \
                 dfuj['positive_above_90_days_after_3rd_dose']

dfuj = dfuj.rename(columns = {'Sum_positive_without_vaccination': 'Oltatlan', 'Age_group': 'Korcsoport' }, inplace = False)
dfuj['Dátum'] = dfuj.apply(lambda row: row['Week'][0:10], axis=1)
dfuj['Dátum'] = pd.to_datetime(dfuj['Dátum'], format='%Y-%m-%d') + pd.Timedelta("3 days") # csütörtök hétfő helyett (hét közepe)
dfuj = dfuj[['Dátum', 'Korcsoport', 'Oltatlan', 'Oltott']]

dfuj = dfuj.groupby("Dátum").sum().reset_index()
dfuj = dfuj[['Dátum', 'Oltatlan']].rename(columns = {'Oltatlan': 'Oltatlan fertőzöttek'}, inplace = False)


# események tábla

dfevnt = pd.read_csv(BASEDIR + "/event-among-vaccinated.csv")

dfevnt = dfevnt.fillna(0)

EVT_COLUMN_LIST = ["event_after_1st_dose", "event_after_2nd_dose", "event_after_3rd_dose", "event_for_not_vaccinated"]

for column in EVT_COLUMN_LIST:
    dfevnt[column] = dfevnt.apply(lambda row: smallerThan5Random(row[column]), axis=1)


for column in EVT_COLUMN_LIST:
    dfevnt[column] = dfevnt[column].astype(float)
    dfevnt[column] = dfevnt[column].astype(int)


dfevnt['Oltott'] = dfevnt['event_after_1st_dose'] + dfevnt['event_after_2nd_dose'] + dfevnt['event_after_3rd_dose']
dfevnt = dfevnt.rename(columns = {'event_for_not_vaccinated': 'Oltatlan', 'Age_group': 'Korcsoport' }, inplace = False)

dfevnt['Dátum'] = dfevnt.apply(lambda row: row['Week'][0:10], axis=1)
dfevnt['Dátum'] = pd.to_datetime(dfevnt['Dátum'], format='%Y-%m-%d') + pd.Timedelta("3 days") # csütörtök hétfő helyett (hét közepe)

dfhalal = dfevnt[dfevnt['Type_of_event'] == 'Death']
dfhalal = dfhalal.groupby("Dátum").sum().reset_index()

dfhalal = dfhalal[['Dátum', 'Oltatlan']].rename(columns = {'Oltatlan': 'Oltatlan halottak'}, inplace = False)

dfuj['Oltatlan halottak'] = dfhalal['Oltatlan halottak']

dfuj["Oltatlan halálozási ráta"] = dfuj["Oltatlan halottak"] / dfuj["Oltatlan fertőzöttek"] * 100

print (dfuj)
quit()




dfevnt['Összes'] = dfevnt['Oltatlan'] + dfevnt['Oltott']



dfcases = pd.read_csv(DATADIR + "data-cases.csv")
dfemergency = pd.read_csv(DATADIR + "data-emergency.csv")
dfdeath = pd.read_csv(DATADIR + "data-death-60.csv")

korcsoportok = dfcases['Korcsoport'].unique()

dfcaseseff = oltottOltatlanTabla(dfcases, korcsoportok[:])
dfdeatheff = oltottOltatlanTabla(dfdeath, korcsoportok[:])

dfoltatlan = dfcaseseff[["Intervallum","Oltatlan"]].rename(columns = {'Oltatlan': 'Oltatlan fertőzöttek'}, inplace = False)
dfoltatlan["Oltatlan halottak"] = dfdeatheff['Oltatlan']
dfoltatlan["Oltatlan halálozási ráta"] = dfoltatlan["Oltatlan halottak"] / dfoltatlan["Oltatlan fertőzöttek"] * 100

pd.plotting.register_matplotlib_converters()

host = host_subplot(111, axes_class=AA.Axes)

par1 = host.twinx()
par2 = host.twinx()

offset = 60
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                    axes=par2,
                                    offset=(offset, 0))
par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)


host.set_xlabel("Intervallum")
host.set_title("COVID oltatlanok halálozási rátája (brit adatok)")
host.set_ylabel("Oltatlan halálozási ráta")
host.set_ylim([0, 0.5])
host.axis[:].major_ticks.set_tick_out(True)
host.axis["top"].major_ticks.set_visible(False)
host.axis["bottom"].major_ticklabels.set_rotation(30)
par1.set_ylabel("Oltatlan fertőzöttek")
par1.set_ylim([0, 400])
par1.axis[:].major_ticks.set_tick_out(True)
par2.set_ylabel("Oltatlan halottak")
par2.set_ylim([0, 900000])
par2.axis[:].major_ticks.set_tick_out(True)

p1, = host.plot(dfoltatlan['Intervallum'], dfoltatlan['Oltatlan halálozási ráta'], label="Oltatlan halálozási ráta")

leg = plt.legend(loc='upper left')

host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())

print (dfoltatlan)

fig = host.get_figure()
fig.savefig(BASEDIR + "/izraeli-járvány-oltatlanok-halálozása.png", bbox_inches = "tight")

quit()


dfcaseseffcs2 = oltottOltatlanTabla(dfcases, korcsoportok[0:2])
dfemergencyeffcs1 = oltottOltatlanTabla(dfemergency, korcsoportok[2:])
dfemergencyeffcs2 = oltottOltatlanTabla(dfemergency, korcsoportok[0:2])
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
ax1.set_ylim([0, 1800000])
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
ax1b.set_ylim([0, 1800000])
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
ax2.set_ylim([0, 12000])
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
ax2b.set_ylim([0, 12000])
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

fig.suptitle('Brit COVID adatok\nOltatlanok halálozása', fontsize=22)
fig.savefig(BASEDIR + "/anglia-oltatlano-halálozása.png")


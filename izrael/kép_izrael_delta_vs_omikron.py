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

def smallerThan5Random(c):
    if c == '<5':
        return str(np.random.randint(4)+1)
    return c

MINX = '2021-07-01'

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
dfuj['Összes'] = dfuj['Oltatlan'] + dfuj['Oltott']
dfuj = dfuj.groupby("Dátum").sum().reset_index()

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

dfevnt['Összes'] = dfevnt['Oltatlan'] + dfevnt['Oltott']

dfkorhaz = dfevnt.copy()
dfkorhaz = dfkorhaz[dfkorhaz['Type_of_event'] == 'Hospitalization']
dfkorhaz = dfkorhaz.groupby("Dátum").sum().reset_index()

dfhalal = dfevnt.copy()
dfhalal = dfhalal[dfhalal['Type_of_event'] == 'Death']
dfhalal = dfhalal.groupby("Dátum").sum().reset_index()


print (dfuj)
# kirajzolás

pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[10,12], constrained_layout=True)

spec = gridspec.GridSpec(ncols=1, nrows=3,
                         width_ratios=[1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1, 1, 1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")
ax1.set_title("Új fertőzések")
ax1.plot(dfuj['Dátum'], dfuj['Összes'], color="lightgreen", label="Oltatlan")
ax1.plot(dfuj['Dátum'], dfuj['Oltott'], color="green", label="Oltott")
ax1.set_ylim([0,300000])
ax1.fill_between(dfuj['Dátum'], dfuj['Összes'], color="lightgreen")
ax1.fill_between(dfuj['Dátum'], dfuj['Oltott'], color="green")

ax1.tick_params(axis='x', rotation=15)
ax1.set_xlim([MINX, dfuj['Dátum'].max()])

ax1.legend( loc = 'upper left' )


ax2=fig.add_subplot(spec[1], label="2")
ax2.set_title("Kórházi kezelés")
ax2.plot(dfkorhaz['Dátum'], dfkorhaz['Összes'], color="#8888ff", label="Oltatlan")
ax2.plot(dfkorhaz['Dátum'], dfkorhaz['Oltott'], color="blue", label="Oltott")
ax2.set_ylim([0,2500])
ax2.fill_between(dfkorhaz['Dátum'], dfkorhaz['Összes'], color="#8888ff")
ax2.fill_between(dfkorhaz['Dátum'], dfkorhaz['Oltott'], color="blue")

ax2.tick_params(axis='x', rotation=15)
ax2.set_xlim([MINX, dfuj['Dátum'].max()])

ax2.legend( loc = 'upper left' )

ax3=fig.add_subplot(spec[2], label="3")
ax3.set_title("Halál")
ax3.plot(dfhalal['Dátum'], dfhalal['Összes'], color="#FF8888", label="Oltatlan")
ax3.plot(dfhalal['Dátum'], dfhalal['Oltott'], color="red", label="Oltott")
ax3.set_ylim([0,250])
ax3.fill_between(dfhalal['Dátum'], dfhalal['Összes'], color="#FF8888")
ax3.fill_between(dfhalal['Dátum'], dfhalal['Oltott'], color="red")

ax3.tick_params(axis='x', rotation=15)
ax3.set_xlim([MINX, dfuj['Dátum'].max()])

ax3.legend( loc = 'upper left' )


fig.suptitle('Izrael: omikron', fontsize=22)
fig.savefig(BASEDIR + "/izraeli-járvány-delta-vs-omikron.png")

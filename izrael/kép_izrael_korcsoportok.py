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

COLORS = [
    '#00FF00', '#00C000', '#0000FF', '#0000C0', '#000080', '#FF0000', '#D80000', '#A80000', '#800000',
]

def smallerThan5Random(c):
    if c == '<5':
        return str(np.random.randint(4)+1)
    return c

def fixSmallerThanFive(dfdata, columns):
    dfdata = dfdata.fillna(0)
    for column in columns:
        dfdata[column] = dfdata.apply(lambda row: smallerThan5Random(row[column]), axis=1)
    for column in columns:
        dfdata[column] = dfdata[column].astype(float)
        dfdata[column] = dfdata[column].astype(int)
    return dfdata

def korcsoportTabla(dfdata):
    csoportok = dfdata['Age_group'].unique()
    dfmerge = None

    for csoport in csoportok:
        csopi = dfdata[dfdata['Age_group'] == csoport].rename(columns = {'all': csoport} )
        csopi = csopi[['Dátum', csoport]].set_index('Dátum')
    
        if dfmerge is None:
            dfmerge = csopi
        else:
            dfmerge[csoport] = csopi[csoport]
    
    dfmerge = dfmerge.reset_index()
    return dfmerge

# új esetek tábla

dfuj = pd.read_csv(BASEDIR + "/cases-among-vaccinated.csv")

COLUMN_LIST = ['positive_1_6_days_after_1st_dose', 'positive_7_13_days_after_1st_dose', 'positive_14_20_days_after_1st_dose', 'positive_above_20_days_after_1st_dose', 'positive_1_6_days_after_2nd_dose',
               'positive_7_13_days_after_2nd_dose', 'positive_14_30_days_after_2nd_dose', 'positive_31_90_days_after_2nd_dose', 'positive_above_3_month_after_2nd_before_3rd_dose', 'positive_1_6_days_after_3rd_dose',
               'positive_7_13_days_after_3rd_dose', 'positive_14_30_days_after_3rd_dose', 'positive_above_90_days_after_3rd_dose', 'Sum_positive_without_vaccination']

dfuj = fixSmallerThanFive(dfuj, COLUMN_LIST)
dfuj['all'] = dfuj[COLUMN_LIST].sum(axis=1)
dfuj['Dátum'] = dfuj.apply(lambda row: row['Week'][0:10], axis=1)
dfuj['Dátum'] = pd.to_datetime(dfuj['Dátum'], format='%Y-%m-%d') + pd.Timedelta("3 days") # csütörtök hétfő helyett (hét közepe)

dfcaseseff = korcsoportTabla(dfuj)

dfesetek = pd.read_csv(BASEDIR + "/event-among-vaccinated.csv")

EVT_COLUMN_LIST = ["event_after_1st_dose", "event_after_2nd_dose", "event_after_3rd_dose", "event_for_not_vaccinated"]

dfesetek = fixSmallerThanFive(dfesetek, EVT_COLUMN_LIST)
dfesetek['all'] = dfesetek[EVT_COLUMN_LIST].sum(axis=1)
dfesetek['Dátum'] = dfesetek.apply(lambda row: row['Week'][0:10], axis=1)
dfesetek['Dátum'] = pd.to_datetime(dfesetek['Dátum'], format='%Y-%m-%d') + pd.Timedelta("3 days") # csütörtök hétfő helyett (hét közepe)

dfemergency = dfesetek[dfesetek['Type_of_event'] == 'Hospitalization']

dfemergencyeff = korcsoportTabla(dfemergency)

dfdeath = dfesetek[dfesetek['Type_of_event'] == 'Death']

dfdeatheff = korcsoportTabla(dfdeath)

pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[9,12], constrained_layout=True)

spec = gridspec.GridSpec(ncols=1, nrows=3,
                         width_ratios=[1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1,1,1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

csoportok = dfuj['Age_group'].unique()

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("A fertőzöttek életkor szerinti eloszlása")

ndx = 0
for csn in csoportok:
  ax1.plot(dfcaseseff['Dátum'], dfcaseseff[csn], label=csn, color = COLORS[ndx])
  ndx += 1
ax1.set(xlabel="Dátum", ylabel="Esetek száma")
ax1.tick_params(axis='x', rotation=20)
ax1.legend()

ax2=fig.add_subplot(spec[1], label="2")

ax2.set_title("A kórházi esetek életkor szerinti eloszlása")

ndx = 0
for csn in csoportok:
  ax2.plot(dfemergencyeff['Dátum'], dfemergencyeff[csn], label=csn, color = COLORS[ndx])
  ndx += 1
ax2.set(xlabel="Dátum", ylabel="Esetek száma")
ax2.tick_params(axis='x', rotation=20)
ax2.legend()

ax3=fig.add_subplot(spec[2], label="3")

ax3.set_title("A halálesetek életkor szerinti eloszlása")

ndx = 0
for csn in csoportok:
  ax3.plot(dfdeatheff['Dátum'], dfdeatheff[csn], label=csn, color = COLORS[ndx])
  ndx += 1
ax3.set(xlabel="Dátum", ylabel="Esetek száma")
ax3.tick_params(axis='x', rotation=20)
ax3.legend()

fig.suptitle('Izraeli COVID adatok\nKorcsoport szerinti eloszlás', fontsize=22)
fig.savefig(BASEDIR + "/izraeli-járvány-eloszlás.png")

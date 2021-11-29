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

FIATAL_KORCSOPORT_NEVE = "20"
FIATAL_KORCSOPORT = ['0-19']

def smallerThan5Random(c):
    if c == '<5':
        return str(np.random.randint(4)+1)
    return c

df = pd.read_csv(BASEDIR +"/vaccinated.csv", parse_dates=['date'])

# oltásadatok előállítása

df = df.rename(columns = {'date': 'Dátum', 'people_vaccinated': '1x oltott', 'people_fully_vaccinated': '2x oltott', 'total_boosters': '3x oltott' }, inplace = False)
df['3x oltott'] = df['3x oltott'].astype(float)
df['3x oltott'] = df['3x oltott'].replace(0, np.NaN)
df['2x oltott'] = df['2x oltott'].replace(0, np.NaN)

# új esetek tábla

dfuj = pd.read_csv(BASEDIR + "/cases-among-vaccinated.csv")
dfuj = dfuj.fillna(0)

COLUMN_LIST = ['positive_1_6_days_after_1st_dose', 'positive_7_13_days_after_1st_dose', 'positive_14_20_days_after_1st_dose', 'positive_above_20_days_after_1st_dose', 'positive_1_6_days_after_2nd_dose',
               'positive_7_13_days_after_2nd_dose', 'positive_14_30_days_after_2nd_dose', 'positive_31_90_days_after_2nd_dose', 'positive_above_90_days_after_2nd_dose', 'positive_1_6_days_after_3rd_dose',
               'positive_7_13_days_after_3rd_dose', 'positive_14_20_days_after_3rd_dose', 'positive_above_20_days_after_3rd_dose', 'Sum_positive_without_vaccination']

for column in COLUMN_LIST:
    dfuj[column] = dfuj.apply(lambda row: smallerThan5Random(row[column]), axis=1)

for column in COLUMN_LIST:
    dfuj[column] = dfuj[column].astype(float)
    dfuj[column] = dfuj[column].astype(int)
    
dfuj['Oltott'] = dfuj['positive_1_6_days_after_1st_dose'] + dfuj['positive_7_13_days_after_1st_dose'] + dfuj['positive_14_20_days_after_1st_dose'] + dfuj['positive_above_20_days_after_1st_dose'] + \
                 dfuj['positive_1_6_days_after_2nd_dose'] + dfuj['positive_7_13_days_after_2nd_dose'] + dfuj['positive_14_30_days_after_2nd_dose'] + dfuj['positive_31_90_days_after_2nd_dose'] + \
                 dfuj['positive_above_90_days_after_2nd_dose'] + dfuj['positive_1_6_days_after_3rd_dose'] + dfuj['positive_7_13_days_after_3rd_dose'] + dfuj['positive_14_20_days_after_3rd_dose'] + \
                 dfuj['positive_above_20_days_after_3rd_dose']

dfuj = dfuj.rename(columns = {'Sum_positive_without_vaccination': 'Oltatlan', 'Age_group': 'Korcsoport' }, inplace = False)
dfuj['Dátum'] = dfuj.apply(lambda row: row['Week'][0:10], axis=1)
dfuj['Dátum'] = pd.to_datetime(dfuj['Dátum'], format='%Y-%m-%d') + pd.Timedelta("3 days") # csütörtök hétfő helyett (hét közepe)
dfuj = dfuj[['Dátum', 'Korcsoport', 'Oltatlan', 'Oltott']]

dfuj20alatt = dfuj.copy()
dfuj20alatt = dfuj20alatt[dfuj20alatt['Korcsoport'].isin(FIATAL_KORCSOPORT)]
dfuj20alatt = dfuj20alatt.groupby("Dátum").sum().reset_index()
dfuj20alatt['Összes'] = dfuj20alatt['Oltatlan'] + dfuj20alatt['Oltott']

dfuj20felett = dfuj.copy()
dfuj20felett = dfuj20felett[~dfuj20felett['Korcsoport'].isin(FIATAL_KORCSOPORT)]

dfuj20felett = dfuj20felett.groupby("Dátum").sum().reset_index()
dfuj20felett['Összes'] = dfuj20felett['Oltatlan'] + dfuj20felett['Oltott']


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

dfkorhaz20alatt = dfevnt.copy()
dfkorhaz20alatt = dfkorhaz20alatt[dfkorhaz20alatt['Type_of_event'] == 'Hospitalization']
dfkorhaz20alatt = dfkorhaz20alatt[dfkorhaz20alatt['Korcsoport'].isin(FIATAL_KORCSOPORT)]
dfkorhaz20alatt = dfkorhaz20alatt.groupby("Dátum").sum().reset_index()

dfkorhaz20felett = dfevnt.copy()
dfkorhaz20felett = dfkorhaz20felett[dfkorhaz20felett['Type_of_event'] == 'Hospitalization']
dfkorhaz20felett = dfkorhaz20felett[~dfkorhaz20felett['Korcsoport'].isin(FIATAL_KORCSOPORT)]
dfkorhaz20felett = dfkorhaz20felett.groupby("Dátum").sum().reset_index()

dfhalal20alatt = dfevnt.copy()
dfhalal20alatt = dfhalal20alatt[dfhalal20alatt['Type_of_event'] == 'Death']
dfhalal20alatt = dfhalal20alatt[dfhalal20alatt['Korcsoport'].isin(FIATAL_KORCSOPORT)]
dfhalal20alatt = dfhalal20alatt.groupby("Dátum").sum().reset_index()

dfhalal20felett = dfevnt.copy()
dfhalal20felett = dfhalal20felett[dfhalal20felett['Type_of_event'] == 'Death']
dfhalal20felett = dfhalal20felett[~dfhalal20felett['Korcsoport'].isin(FIATAL_KORCSOPORT)]

dfhalal20felett = dfhalal20felett.groupby("Dátum").sum().reset_index()


# kirajzolás

pd.plotting.register_matplotlib_converters()

fig = plt.figure(figsize=[12,9.5], constrained_layout=True)

spec = gridspec.GridSpec(ncols=2, nrows=4,
                         width_ratios=[1, 1,], wspace=0.3,
                         hspace=0.38, height_ratios=[1, 1, 1, 1], figure = fig)
spec.update(left=0.06,right=0.99,top=1,bottom=0.01,wspace=0.25,hspace=0.35)

ax1=fig.add_subplot(spec[0], label="1")

ax1.set_title("COVID oltottak")

ax1.plot(df['Dátum'], df['1x oltott'], color="green", label="1x oltott")
ax1.plot(df['Dátum'], df['2x oltott'], color="magenta", label="2x oltott")
ax1.plot(df['Dátum'], df['3x oltott'], color="blue", label="3x oltott")
ax1.set_ylim([0,6500000])
ax1.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax1.legend()

ax1.tick_params(axis='x', rotation=15)

ax2=fig.add_subplot(spec[1], label="2")

ax2.set_title("COVID oltottak")

ax2.plot(df['Dátum'], df['1x oltott'], color="green", label="1x oltott")
ax2.plot(df['Dátum'], df['2x oltott'], color="magenta", label="2x oltott")
ax2.plot(df['Dátum'], df['3x oltott'], color="blue", label="3x oltott")
ax2.set_ylim([0,6500000])
ax2.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax2.legend()

ax2.tick_params(axis='x', rotation=15)

ax3=fig.add_subplot(spec[2], label="3")
ax3.set_title("Új fertőzések " + FIATAL_KORCSOPORT_NEVE + " év felett, sok oltott")
ax3.plot(dfuj20felett['Dátum'], dfuj20felett['Összes'], color="lightgreen", label="Összes")
ax3.plot(dfuj20felett['Dátum'], dfuj20felett['Oltott'], color="green", label="Oltott")
ax3.set_ylim([0,36000])
ax3.fill_between(dfuj20felett['Dátum'], dfuj20felett['Összes'], color="lightgreen")
ax3.fill_between(dfuj20felett['Dátum'], dfuj20felett['Oltott'], color="green")

ax3.tick_params(axis='x', rotation=15)
ax3.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax3.legend()

ax4=fig.add_subplot(spec[3], label="4")
ax4.set_title("Új fertőzések " + FIATAL_KORCSOPORT_NEVE + " év alatt, kevés oltott")
ax4.plot(dfuj20alatt['Dátum'], dfuj20alatt['Összes'], color="lightgreen", label="Összes")
ax4.plot(dfuj20alatt['Dátum'], dfuj20alatt['Oltott'], color="green", label="Oltott")
ax4.set_ylim([0,36000])
ax4.fill_between(dfuj20alatt['Dátum'], dfuj20alatt['Összes'], color="lightgreen")
ax4.fill_between(dfuj20alatt['Dátum'], dfuj20alatt['Oltott'], color="green")

ax4.tick_params(axis='x', rotation=15)
ax4.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax4.legend()

ax5=fig.add_subplot(spec[4], label="5")
ax5.set_title("Kórházi kezelés " + FIATAL_KORCSOPORT_NEVE + " év felett, sok oltott")
ax5.plot(dfkorhaz20felett['Dátum'], dfkorhaz20felett['Összes'], color="#8888ff", label="Összes")
ax5.plot(dfkorhaz20felett['Dátum'], dfkorhaz20felett['Oltott'], color="blue", label="Oltott")
ax5.set_ylim([0,1900])
ax5.fill_between(dfkorhaz20felett['Dátum'], dfkorhaz20felett['Összes'], color="#8888ff")
ax5.fill_between(dfkorhaz20felett['Dátum'], dfkorhaz20felett['Oltott'], color="blue")

ax5.tick_params(axis='x', rotation=15)
ax5.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax5.legend()

ax6=fig.add_subplot(spec[5], label="6")
ax6.set_title("Kórházi kezelés " + FIATAL_KORCSOPORT_NEVE + " év alatt, kevés oltott")
ax6.plot(dfkorhaz20alatt['Dátum'], dfkorhaz20alatt['Összes'], color="#8888ff", label="Összes")
ax6.plot(dfkorhaz20alatt['Dátum'], dfkorhaz20alatt['Oltott'], color="blue", label="Oltott")
ax6.set_ylim([0,1900])
ax6.fill_between(dfkorhaz20alatt['Dátum'], dfkorhaz20alatt['Összes'], color="#8888ff")
ax6.fill_between(dfkorhaz20alatt['Dátum'], dfkorhaz20alatt['Oltott'], color="blue")

ax6.tick_params(axis='x', rotation=15)
ax6.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax6.legend()

ax7=fig.add_subplot(spec[6], label="7")
ax7.set_title("Halál " + FIATAL_KORCSOPORT_NEVE + " év felett, sok oltott")
ax7.plot(dfhalal20felett['Dátum'], dfhalal20felett['Összes'], color="#FF8888", label="Összes")
ax7.plot(dfhalal20felett['Dátum'], dfhalal20felett['Oltott'], color="red", label="Oltott")
ax7.set_ylim([0,400])
ax7.fill_between(dfhalal20felett['Dátum'], dfhalal20felett['Összes'], color="#FF8888")
ax7.fill_between(dfhalal20felett['Dátum'], dfhalal20felett['Oltott'], color="red")

ax7.tick_params(axis='x', rotation=15)
ax7.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax7.legend()

ax8=fig.add_subplot(spec[7], label="8")
ax8.set_title("Halál " + FIATAL_KORCSOPORT_NEVE + " év alatt, kevés oltott")
ax8.plot(dfhalal20alatt['Dátum'], dfhalal20alatt['Összes'], color="#FF8888", label="Összes")
ax8.plot(dfhalal20alatt['Dátum'], dfhalal20alatt['Oltott'], color="red", label="Oltott")
ax8.set_ylim([0,400])
ax8.fill_between(dfhalal20alatt['Dátum'], dfhalal20alatt['Összes'], color="#FF8888")
ax8.fill_between(dfhalal20alatt['Dátum'], dfhalal20alatt['Oltott'], color="red")

ax8.tick_params(axis='x', rotation=15)
ax8.set_xlim([df['Dátum'].min(), df['Dátum'].max()])

ax8.legend()

fig.suptitle('Izraeli COVID járvány (Pfizer+Moderna)', fontsize=22)
fig.savefig(BASEDIR + "/izraeli-járvány.png")

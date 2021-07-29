#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from pandas.plotting import table
import matplotlib.pyplot as plt

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/stadat-halalozas-elokeszitve.csv", parse_dates=['A hét kező napja', 'A hét záró napja'], delimiter=';')
dfweeks = df[(df['A hét sorszáma'] < 26.0) | (df['A hét sorszáma'] > 35.0)]

df2020 = dfweeks[dfweeks['A hét záró napja'] > "2020-08-30"]
covid_elhunytak = df2020[['A hét kező napja', 'A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'Elhunytak'}, inplace = False)

dfatlag = dfweeks[dfweeks['A hét záró napja'] < "2020-01-01"]

dfatlag = dfatlag.groupby('A hét sorszáma').mean().reset_index()
atlag_elhunytak = dfatlag[['A hét sorszáma', 'Összesen összesen']].rename(columns = {'Összesen összesen': 'KSH 5 éves átlag'}, inplace = False)

dfkozos = pd.merge(covid_elhunytak, atlag_elhunytak, left_on = 'A hét sorszáma', right_on = 'A hét sorszáma')
dfkozos = dfkozos.rename(columns = {'A hét kező napja': 'Dátum'}, inplace = False)
dfkozos['KSH többlet']=dfkozos['Elhunytak'] - dfkozos['KSH 5 éves átlag']

datemax = dfkozos['Dátum'].max()

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])
df['Dátum'] = df.apply(lambda row: row['Dátum'] - dt.timedelta(days=row['Dátum'].weekday()), axis=1)
dfheti = (df.groupby('Dátum', as_index=False).sum())
dfheti = dfheti.rename(columns = {'Napi új elhunyt': "Hivatalos heti új elhunyt", 'Hét kezdet': 'Dátum'}, inplace = False)
dfheti = dfheti[(dfheti['Dátum'] <= datemax) & (dfheti['Dátum'] > "2020-08-30")]

dfkozos = pd.merge(dfkozos, dfheti, left_on = 'Dátum', right_on = 'Dátum')


df1h = dfkozos[dfkozos['Dátum'] < "2021-02-01"]
df2h = dfkozos[dfkozos['Dátum'] >= "2021-02-01"]

sum1h = df1h.sum()
sum2h = df2h.sum()

h1ksh = int(sum1h['KSH többlet'] + 0.5) 
h2ksh = int(sum2h['KSH többlet'] + 0.5) 

h1covid = int(sum1h['Hivatalos heti új elhunyt']) 
h2covid = int(sum2h['Hivatalos heti új elhunyt']) 


fig = plt.figure(figsize=[2.5,1.8])
ax = fig.add_subplot(111)
ax.set_title('A hullámok összehasonlítása COVID adatok és KSH alapján', fontsize = 12)
oszlopok = ['2. hullám', '3. hullám', 'Összesen']
sorok = ['KSH többlet', 'COVID adatok']
ertekek = [[h1ksh, h2ksh, h1ksh+h2ksh], [h1covid, h2covid, h1covid+h2covid]]

# Tábla elkészítése
a_tabla = plt.table(cellText=ertekek,
                      colWidths=[0.1] * 3,
                      rowLabels=sorok,
                      colLabels=oszlopok,
                      loc='center')
a_tabla.auto_set_font_size(False)
a_tabla.set_fontsize(18)
a_tabla.scale(7, 2.5)

# Removing ticks and spines enables you to get the figure only with table
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)
plt.savefig(BASEDIR + "/képek/KshVsHivatalosCovidHalálozásTábla.png", bbox_inches='tight', pad_inches=0.05)

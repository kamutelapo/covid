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

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/újfertőzések.csv", parse_dates=['Dátum'])

summa = df.sum()

rate = int(100.0 * summa['Legalább 1 oltással rendelkezők száma'] / summa['Regisztrált fertőzöttek száma'] + 0.5)

pd.plotting.register_matplotlib_converters()

fig=plt.figure(figsize=[6,4])

spec = gridspec.GridSpec(ncols=1, nrows=1,
                         width_ratios=[1], wspace=0.3,
                         hspace=0.40, height_ratios=[1])
spec.update(left=0.06,right=0.95,top=0.92,bottom=0.08,wspace=0.25,hspace=0.50)

ax1=fig.add_subplot(spec[0], label="1")
ax1.set_title("Magyar COVID adatok az új fertőzöttekről (" + str(rate) + "% oltott)")
ax1.plot(df['Dátum'], df['Regisztrált fertőzöttek száma'], color='#7070FF', label='Regisztrált fertőzöttek száma')
ax1.plot(df['Dátum'], df['Legalább 1 oltással rendelkezők száma'], color='darkblue', label='Legalább 1 oltással rendelkezők száma')
ax1.fill_between(df['Dátum'], df['Regisztrált fertőzöttek száma'], color="#7070FF")
ax1.fill_between(df['Dátum'], df['Legalább 1 oltással rendelkezők száma'], color="darkblue")
ax1.set_ylim([0, 5000])
ax1.legend()

fig.savefig(BASEDIR + "/Magyar.png", bbox_inches = "tight")

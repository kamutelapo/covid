#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt

BASEDIR=os.path.dirname(__file__)

df = pd.read_csv(BASEDIR +"/adatok/hiradatok.csv", parse_dates=['Dátum'])

df['Lélegeztetettek'] = df['Lélegeztetettek'].interpolate(method='linear')

plot = df.plot(x='Dátum', y='Lélegeztetettek', title="Lélegeztetettek száma")	

fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Lélegeztetettek.png", bbox_inches = "tight")

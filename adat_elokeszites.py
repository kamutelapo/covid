#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

BASEDIR=os.path.dirname(__file__)

csv1 = pd.read_csv(BASEDIR +"/covidadatok1.csv")
csv2 = pd.read_csv(BASEDIR +"/covidadatok2.csv")

csvconcat = pd.concat([csv1, csv2], sort=True)
csvconcat = csvconcat.replace(np.nan, '0', regex=True)

csvout = csvconcat[["Dátum", "Aktív fertőzött", "Elhunyt", "Gyógyult", "Összesen", "Beoltottak", "Aktív fertőzöttek változása", "Napi új elhunyt", "Napi új gyógyult", "Napi új fertőzött", "Napi új beoltott"]]

csvout.to_csv(BASEDIR +"/covidadatok.csv", index = False)


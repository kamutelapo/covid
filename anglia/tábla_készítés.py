#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import pandas as pd

BASEDIR=os.path.dirname(__file__)
DATADIR=BASEDIR + "/adatok/"

cases = []
emergency = []
death28 = []
death60 = []

def importData(week):
    pass

for week in range(36, 53):
    if os.path.exists(DATADIR + "week-" + str(week) + "-cases.csv"):
        print ("A " + str(week) + ". hét importálása...")
        importData(week)  



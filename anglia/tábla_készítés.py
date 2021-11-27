#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import pandas as pd

BASEDIR=os.path.dirname(__file__)
DATADIR=BASEDIR + "/adatok/"

MERGE_COLUMNS = {
    "cases": [
        "Cases rate vaccinated",
        "Cases rate not vaccinated"
    ],
}

cases = []
emergency = []
death28 = []
death60 = []

def addData(week, dtype):
    dfdata = pd.read_csv(DATADIR + "week-" + str(week) + "-" + dtype + ".csv")
    dfrates = None
    if os.path.exists(DATADIR + "week-" + str(week) + "-rates.csv"):
        dfrates = pd.read_csv(DATADIR + "week-" + str(week) + "-rates.csv")
        dfrateext = dfrates[['Age group'] + MERGE_COLUMNS[dtype]]
        dfdata["Rate vaccinated"] = dfrateext[MERGE_COLUMNS[dtype][0]]
        dfdata["Rate not vaccinated"] = dfrateext[MERGE_COLUMNS[dtype][1]]

    array = dfdata.to_numpy()    

    result = []
    for row in array:
        rowd = [week, str(week - 4) + "-" + str(week - 1)]
        rowd.extend(row)
        
        
        result.append(rowd)

    return result

def importData(week):
    cases.extend(addData(week, "cases"))

for week in range(36, 53):
    if os.path.exists(DATADIR + "week-" + str(week) + "-cases.csv"):
        #print ("A " + str(week) + ". hét importálása...")
        importData(week)  

dfcases = pd.DataFrame(cases, columns=['Hét', 'Intervallum', 'Korcsoport', 'Összes', 'TB-n kívül', 'Oltatlan', 'Egyszer oltott (1-20)', 'Egyszer oltott (21-)', 'Kétszer oltott', 'Kétszer oltottak aránya', 'Oltatlanok aránya'])
dfcases.to_csv(DATADIR + "data-cases.csv", index = False)

#pd.set_option("display.max_rows", None)
#print (dfcases)

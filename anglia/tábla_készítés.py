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
    "emergency": [
        "Emergency rate vaccinated",
        "Emergency rate not vaccinated"
    ],
    "death-28": [
        "Deaths28 rate vaccinated",
        "Deaths28 rate not vaccinated"
    ],
    "death-60": [
        "Deaths60 rate vaccinated",
        "Deaths60 rate not vaccinated"
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
        weekmin = week - 4
        weekmax = week - 1
        
        if weekmin > 51:
            weekmin -= 51
        if weekmax > 51:
            weekmax -= 51
        
        rowd = [week, str(weekmin) + "-" + str(weekmax)]
        rowd.extend(row)

        for i in range(0, len(rowd)):
            rowd[i] = str(rowd[i]).replace(",", "")
        
        result.append(rowd)

    return result

def importData(week):
    cases.extend(addData(week, "cases"))
    emergency.extend(addData(week, "emergency"))
    death28.extend(addData(week, "death-28"))
    death60.extend(addData(week, "death-60"))

for week in range(36, 53):
    if os.path.exists(DATADIR + "week-" + str(week) + "-cases.csv"):
        #print ("A " + str(week) + ". hét importálása...")
        importData(week)  

dfcases = pd.DataFrame(cases, columns=['Hét', 'Intervallum', 'Korcsoport', 'Összes', 'TB-n kívül', 'Oltatlan', 'Egyszer oltott (1-20)', 'Egyszer oltott (21-)', 'Kétszer oltott', 'Kétszer oltottak aránya', 'Oltatlanok aránya'])
dfcases.to_csv(DATADIR + "data-cases.csv", index = False)
dfemergency = pd.DataFrame(emergency, columns=['Hét', 'Intervallum', 'Korcsoport', 'Összes', 'TB-n kívül', 'Oltatlan', 'Egyszer oltott (1-20)', 'Egyszer oltott (21-)', 'Kétszer oltott', 'Kétszer oltottak aránya', 'Oltatlanok aránya'])
dfemergency.to_csv(DATADIR + "data-emergency.csv", index = False)
dfdeath28 = pd.DataFrame(death28, columns=['Hét', 'Intervallum', 'Korcsoport', 'Összes', 'TB-n kívül', 'Oltatlan', 'Egyszer oltott (1-20)', 'Egyszer oltott (21-)', 'Kétszer oltott', 'Kétszer oltottak aránya', 'Oltatlanok aránya'])
dfdeath28.to_csv(DATADIR + "data-death-28.csv", index = False)
dfdeath60 = pd.DataFrame(death60, columns=['Hét', 'Intervallum', 'Korcsoport', 'Összes', 'TB-n kívül', 'Oltatlan', 'Egyszer oltott (1-20)', 'Egyszer oltott (21-)', 'Kétszer oltott', 'Kétszer oltottak aránya', 'Oltatlanok aránya'])
dfdeath60.to_csv(DATADIR + "data-death-60.csv", index = False)

#pd.set_option("display.max_rows", None)
#print (dfcases)

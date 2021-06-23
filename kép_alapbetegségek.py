#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import os
import re

BASEDIR=os.path.dirname(__file__)


df = pd.read_csv(BASEDIR +"/elhunytak_datummal.csv", parse_dates=['Dátum'])

betegsegek = {}

for btga in df['Alapbetegségek']:
    btgtomb = re.split("\s*[,;]\s*", btga)
    
    for btg in btgtomb:
        btg = btg.lower()
        
        if 'cukorbeteg' in btg or 'cukorbetg' in btg or 'cukorbt' in btg:
            btg = 'cukorbetegség'
        if 'diabetes' in btg or 'diabétesz' in btg:
            btg = 'cukorbetegség'
        if 'magasvérnyomás' in btg or 'magas vérnyomás' in btg or 'magasvényomás' in btg or 'magas vényomás' in btg \
            or 'magasv érnyomás' in btg or 'magas vérnomás' in btg or 'magas vérnoymás' in btg or 'magasvérnoymás' in btg:
                btg = 'magas vérnyomás'
        if 'elhízás' in btg:
            btg = 'elhízás'
        if 'veseelégtelenség' in btg or 'vese elégtelenség' in btg or 'vese betegség' in btg or 'vesebetegség' in btg \
            or 'veseelégteleség' in btg or 'veselégtelenség' in btg or 'veseelégtelensség' in btg:
                btg = 'veseelégtelenség'
        if 'nem ismert alapbetegség' in btg or btg == 'nem ismert' or 'nincs ismert betegség' in btg \
            or 'nincs ismert betegség' in btg or 'nincs ismert alapbetegség' in btg or 'betegsége nem ismert' in btg \
            or 'betegsége nem volt' in btg or 'jelenleg nem ismert' == btg:
                btg = 'nem ismert alapbetegség'
        if 'szívbetegség' in btg or 'szívbillenty' in btg or 'szívbeegség' in btg:
            btg = 'szívbetegség'
        if 'daganat' in btg or 'dagantos' in btg:
            btg = 'daganatos megbetegedés'
        if 'tüdõbetegség' in btg or 'tüdőbetegség' in btg:
            btg = 'tüdőbetegség'
        if 'demencia' in btg or 'dementia' in btg or 'demecia' in btg:
            btg = 'demencia'
        if 'szívritmuszavar' in btg or 'pitvarfibrilláció' in btg or ('pitvar' in btg and 'fibrilláció' in btg) \
            or btg in ('pitvarfibrillácó', 'pitvarfibrillació', 'pitvarfibriláció', 'pitvarfibrillatio', 'pitvarremegés', 'pitvarfibrillatió','pitvari fibrillació', 'pitvarfiblláció', 'pitvari fibrillatio és flutter', 
            'ritmuszavar', 'ritmusszabályzóval élő személy', 'szívritmuszvar', 'szivritmuszavar') \
            or 'szívritmus' in btg:
            btg = 'szívritmuszavar'
        if 'vérszegénység' in btg or btg in ('vérszegényég','vérszegésnység'):
            btg = 'vérszegénység'
        if 'meszesedés' in btg or btg in ('érelmeszsedés', 'agyérelmeszedés', 'általános érelmeszedés'):
            btg = 'érelmeszesedés'
        if 'szívelégtelenség' in btg or btg in ('szívelégtelenég', 'szívelégetelenség', 'szíveleégtelenség',
                                                'szívelégelenség', 'szívelégtlenség'):
            btg = 'szívelégtelenség'
        if 'asztma' in btg or 'asthma' in btg:
            btg = 'asztma'
        if 'infarktus' in btg or 'infarctus' in btg:
            btg = 'infarktus'
        if 'parkinson' in btg or 'parkinzon' in btg or 'parkinsor' in btg:
            btg = 'parkinson-kór'
        if 'stroke' in btg:
            btg = 'stroke'
        
        if btg not in betegsegek:
            betegsegek[btg]=1
        else:
            betegsegek[btg]=betegsegek[btg]+1


fobb_alapbetegsegek=[]

for k in betegsegek:
    if betegsegek[k] > 500:
        fobb_alapbetegsegek.append([k, betegsegek[k]])

fobb_alapbetegsegek.sort(key=lambda x: x[1])

df = pd.DataFrame(fobb_alapbetegsegek, columns=['Alapbetegség','Szám'])

plot = df.plot.barh(x='Alapbetegség', y='Szám', title="Főbb alapbetegségek a COVID elhunytak között")
fig = plot.get_figure()
fig.savefig(BASEDIR + "/képek/Alapbetegségek.png", bbox_inches = "tight")

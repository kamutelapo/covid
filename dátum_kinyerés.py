#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

file1 = open(sys.argv[1], 'r', encoding='utf-8', errors='ignore')
lines = file1.readlines()
file1.close()

pattern = re.compile(r'^\s*(\d\d\d\d)\.\s+(\w+)\s+(\d+)\.\s+\-.*$')

match = None

for line in lines:
    mtch = pattern.match(line)
    if mtch:
        match = mtch
        break

if match is None:
    raise Exception("Nincs dátum!")


date_map = {"január":"01", "február":"02", "március":"03", "április":"04", "május":"05", "június":"06", "július":"07", "augusztus":"08", "szeptember":"09", "október":"10", "november":"11", "december":"12"}

date = match.group(1) + "-" + date_map[match.group(2)] + "-" + match.group(3)
print (date)

exit(0)

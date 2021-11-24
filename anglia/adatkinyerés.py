#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

FILEDIR=sys.argv[1]

for filename in os.listdir(FILEDIR):
  if filename.endswith(".txt"): 
    path = os.path.join(FILEDIR, filename)
    print (path)


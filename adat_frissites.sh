#!/bin/bash
set -e
set -o pipefail

ELHUNYTAK=1

if [ "$1" == "-l" ]; then
  ELHUNYTAK=0
fi

./covid_adatok_letoltes.sh
./adat_kinyerés.py
if [ $ELHUNYTAK != 0 ]; then
  ./covid_elhunytak_letoltes.sh
  ./adat_elokeszites.py
fi
./stat_adat_elokeszites.sh
./képek_készítése.sh

#!/bin/bash
set -e
set -o pipefail

./covid_adatok_letoltes.sh
./adat_kinyerés.py
./covid_elhunytak_letoltes.sh
./adat_elokeszites.py
./stat_adat_elokeszites.sh
./képek_készítése.sh

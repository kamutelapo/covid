#!/bin/bash
wget https://www.ksh.hu/stadat_files/nep/hu/nep0065.csv -O adatok/stadat-halalozas.csv

iconv -f 'ISO 8859-2' -t 'UTF-8' adatok/stadat-halalozas.csv | head -2 | tail -1  >adatok/stadat-halalozas-elokeszitve.csv

iconv -f 'ISO 8859-2' -t 'UTF-8' adatok/stadat-halalozas.csv \
  | sed -e 's/. január /.01./g' \
  | sed -e 's/. február /.02./g' \
  | sed -e 's/. március /.03./g' \
  | sed -e 's/. április /.04./g' \
  | sed -e 's/. május /.05./g' \
  | sed -e 's/. június /.06./g' \
  | sed -e 's/. július /.07./g' \
  | sed -e 's/. augusztus /.08./g' \
  | sed -e 's/. szeptember /.09./g' \
  | sed -e 's/. október /.10./g' \
  | sed -e 's/. november /.11./g' \
  | sed -e 's/. december /.12./g' \
  | sed -e 2d \
  | sed -e 's/ //g' >>adatok/stadat-halalozas-elokeszitve.csv

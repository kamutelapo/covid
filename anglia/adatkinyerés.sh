#!/bin/bash
TEMP_DIR=$(mktemp -d -t covidanglia-XXXXXXXXXX)
echo "Adatok kinyerése a PDF fájlokból a $TEMP_DIR könyvtárba..."

FOKONYVTAR=`dirname $0`

for fname in `ls $FOKONYVTAR/pdf`; do
  echo Feldolgozás: $fname...
  tfname=${fname%.pdf}.txt
  pdftotext $FOKONYVTAR/pdf/$fname $TEMP_DIR/$tfname
done

echo "Tábla készítése..."
$FOKONYVTAR/adatkinyerés.py $TEMP_DIR

#!/bin/bash
TEMP_DIR=$(mktemp -d -t covidelhunyt-XXXXXXXXXX)
echo "Elhunytak lekérése a $TEMP_DIR könyvtárba..."

for i in `seq 0 10000`; do
  NUMBER=`printf "%04d" $i`
  wget https://koronavirus.gov.hu/elhunytak?page=$i -O $TEMP_DIR/elhunytak$NUMBER.html;
  
  if ! grep Elhunytak $TEMP_DIR/elhunytak$NUMBER.html; then
    rm $TEMP_DIR/elhunytak$NUMBER.html
    break
  fi
done

KESZ_TABLA=`dirname $0`
echo "Tábla felépítése itt: $KESZ_TABLA..."

FILES=`find $TEMP_DIR/ -iname '*elhunytak*' | sort`

OUTPUT_FILE=$KESZ_TABLA/elhunytak.csv
rm $OUTPUT_FILE
echo Sorszám,Nem,Kor,Alapbetegségek > $OUTPUT_FILE

for FILE in $FILES; do
  $KESZ_TABLA/html2csv.py $FILE >>$OUTPUT_FILE
done

csvsort --columns 3,1 $OUTPUT_FILE >$KESZ_TABLA/elhunytak_eletkor.csv

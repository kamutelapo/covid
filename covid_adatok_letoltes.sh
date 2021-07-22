#!/bin/bash
TEMP_DIR=$(mktemp -d -t covidadat-XXXXXXXXXX)
echo "Adatok lekérése a $TEMP_DIR könyvtárba..."

let hir=1

FOKONYVTAR=`dirname $0`
KESZ_TABLA="$FOKONYVTAR/adatok"
echo "Tábla felépítése itt: $KESZ_TABLA..."

OUTPUT_FILE=$KESZ_TABLA/nyersadatok.txt
rm $OUTPUT_FILE
echo  > $OUTPUT_FILE

for i in `seq 0 10000`; do
  NUMBER=`printf "%04d" $i`
  wget https://koronavirus.gov.hu/hirek?page=$i -O $TEMP_DIR/hirek$NUMBER.html;
  
  AKTIV_LAP='<li class="active"><span>'$((i+1))'</span></li>'
  
  if ! grep "$AKTIV_LAP" $TEMP_DIR/hirek$NUMBER.html; then
    rm $TEMP_DIR/hirek$NUMBER.html
    break
  fi
  
  for href in `cat $TEMP_DIR/hirek$NUMBER.html | grep -1 -E 'aktualis_a|01304724o|00cikk_[0-9]{1,4}|koronavirus_bejelentes|adatok.png|00cikk.png|adatok_[0-9]{1,4}' | grep href | awk -F '"' '{print $2}'`; do
    HIRNUMBER=`printf "%04d" $hir`
    wget https://koronavirus.gov.hu$href -O $TEMP_DIR/hir$HIRNUMBER.html;
    html2text -utf8 $TEMP_DIR/hir$HIRNUMBER.html >$TEMP_DIR/hir$HIRNUMBER.txt
    
    $FOKONYVTAR/dátum_kinyerés.py $TEMP_DIR/hir$HIRNUMBER.txt
    if [ $? != 0 ]; then
      exit 1
    fi
    
    DATUM=`$FOKONYVTAR/dátum_kinyerés.py $TEMP_DIR/hir$HIRNUMBER.txt`
    echo >> $OUTPUT_FILE
    echo >> $OUTPUT_FILE
    echo "##### $DATUM" >> $OUTPUT_FILE
    echo >> $OUTPUT_FILE
    echo >> $OUTPUT_FILE

    cat $TEMP_DIR/hir$HIRNUMBER.txt >> $OUTPUT_FILE
    
    let hir=hir+1
  done
done

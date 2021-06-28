* [COVID járványelemzés a magyarországi adatok alapján](#covid-járványelemzés-a-magyarországi-adatok-alapján)
   * [Járvány adatok](#járvány-adatok)
      * [Halálozási adatok](#halálozási-adatok)
      * [Elhunytak életkor szerint](#elhunytak-életkor-szerint)
         * [Hivatalos COVID adatok](#hivatalos-covid-adatok)
         * [KSH alapján számolva](#ksh-alapján-számolva)
      * [TBD](#tbd)
   * [Szimulációk](#szimulációk)
      * [Korlátozások](#korlátozások)
      * [Oltások](#oltások)
      * [Következtetés](#következtetés)

# COVID járványelemzés a magyarországi adatok alapján

A projekt célja az, hogy a statisztikai adatok alapján összefogó képet kapjunk arról,
hogy mi történt a 2020-2021-es COVID járvány alatt Magyarországon.

## Járvány adatok

### Halálozási adatok

Az ábrán a hivatalos COVID halálozási adatokat vetjük össze a KSH adatokkal.

![Halálozási adatok](https://github.com/kamutelapo/covid/blob/master/k%C3%A9pek/KshVsHivatalosCovidHal%C3%A1loz%C3%A1s.png?raw=true)

### Elhunytak életkor szerint

#### Hivatalos COVID adatok

![Elhunytak életkor szerint](https://github.com/kamutelapo/covid/blob/master/k%C3%A9pek/ElhunytakKorcsoportSzerint.png?raw=true)

#### KSH alapján számolva

![Elhunytak életkor szerint](https://github.com/kamutelapo/covid/blob/master/k%C3%A9pek/KshElhunytakKorcsoportSzerint.png?raw=true)

### TBD

## Szimulációk

Ebben a fejezetben megvizsgálom, hogy a korlátozások, oltások milyen hatással vannak a járványgörbe alakjára.

### Korlátozások

A szimulációban bevezetünk egy korlátozást, ami a vírus R értékét felére csökkenti. A végeredmény majdnem
haranggörbe lesz. A korlátozás után a görbe meredek csökkenésbe kezd, majd törést követően beáll az új
R értéknek megfelelő haranggörbére. A korlátozás hatására majdnem haranggörbét kapunk.

![Korlátozás-szimuláció](https://github.com/kamutelapo/covid/blob/master/k%C3%A9pek/Korl%C3%A1toz%C3%A1s-szimul%C3%A1ci%C3%B3.png?raw=true)

### Oltások

A szimulációban azt nézzük meg, hogy az oltás hatása mennyiben változtatja meg a járványgörbe alakját.
A végeredmény az, hogy a fokozatos oltás szintén haranggörbét eredményez, ami logikus is, hiszen
csak az R érték csökken.

![Oltás-szimuláció](https://github.com/kamutelapo/covid/blob/master/k%C3%A9pek/Olt%C3%A1s-szimul%C3%A1ci%C3%B3.png?raw=true)

### Következtetés

Pusztán a járvány-görbe alakján lehetetlen megmondani, hogy hatásosak voltak-e a korlátozások és az oltási kampány.

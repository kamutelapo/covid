#!/usr/bin/perl

use strict;

use Data::Dumper;

use constant EMBEREK_SZAMA => 100000;
use constant COVID_RATA => 1.6;
use constant KEZDO_BETEG => 10;
use constant BETEG_NAPOK => 14;
use constant OLTAS_UTANI_VEDETTSEG => 14;
use constant COVID_RATA_OLTVA => 0.5;


sub betegekSzama($) {
  my ($adatok) = @_;
  return scalar(grep { $_->{beteg} } @{$adatok->{ember}});
}

sub covidCiklus($) {
  my ($adatok) = @_;
  $adatok->{nap}++;
  
  my $oltok = 0;
  while ( ($adatok->{oltasmutato} < EMBEREK_SZAMA) && ($oltok < $adatok->{napi_oltott} ) ) {
    my $ember = $adatok->{ember}[$adatok->{oltasmutato}];

    if ( !$ember->{oltott} && !$ember->{beteg} && !$ember->{gyogyult} ) {
      $ember->{frissenoltott} = OLTAS_UTANI_VEDETTSEG;
      $ember->{oltott} = 1;
      $ember->{covid_esely} = $adatok->{covid_esely_oltas_utan};
      $oltok++;
      $adatok->{oltottak}++;
    }
    $adatok->{oltasmutato}++;
  }
  
  my $betegek = betegekSzama($adatok);
  my $fertozesValoszinuseg = $betegek * COVID_RATA / EMBEREK_SZAMA / BETEG_NAPOK;
  
  if ($adatok->{nap} >= $adatok->{korlatozas_ciklus}) {
    $fertozesValoszinuseg = $fertozesValoszinuseg * $adatok->{korlatozas_erosseg};
  }
  
  my $delta = 0;
  
  for my $ember( @{$adatok->{ember}} ) {
    if ($ember->{frissenoltott}) {
      $ember->{frissenoltott} = $ember->{frissenoltott} - 1;
      $ember->{covid_esely} = $ember->{covid_esely} - $adatok->{covid_delta};
    }
    if ($ember->{beteg}) {
      $ember->{beteg} = $ember->{beteg} - 1;
      if (!$ember->{beteg}) {
        $ember->{gyogyult} = 1;
        $ember->{covid_esely} = 0.0;
        $delta--;
      }
    } else {
      my $igazitott = $fertozesValoszinuseg * $ember->{covid_esely};
      if(rand() <= $igazitott) {
        $ember->{beteg} = BETEG_NAPOK;
        $delta++;
        $adatok->{osszeseset}++;
      }
    }
  }

  my $ujadat = $betegek + $delta;
  push @{$adatok->{napi_ertekek}}, [$ujadat];
  return $ujadat;
}

sub covidSzimulacio(%) {
  my %adatok = @_;
  
  $adatok{napi_oltott} = 0 if ! exists $adatok{napi_oltott};
  $adatok{covid_esely_oltas_utan} = 1.0 if ! exists $adatok{covid_esely_oltas_utan};
  $adatok{covid_delta} = ( $adatok{covid_esely_oltas_utan} - COVID_RATA_OLTVA ) / OLTAS_UTANI_VEDETTSEG;
  $adatok{immunis} = 0 if ! exists $adatok{immunis};
  $adatok{korlatozas_ciklus} = 999999999999 if ! exists $adatok{korlatozas_ciklus};
  $adatok{korlatozas_erosseg} = 1 if ! exists $adatok{korlatozas_erosseg};
 
  $adatok{ember} = [];

  for(my $i=0; $i < EMBEREK_SZAMA; $i++) {
    my $covidEsely = ((rand() * 100.0) < $adatok{immunis}) ? 0.0 : 1.0;
    push @{$adatok{ember}}, { beteg => 0, gyogyult => 0, oltott => 0, covid_esely => $covidEsely };
  }

  for(my $i=0; $i < KEZDO_BETEG; $i++) {
    $adatok{ember}[$i]{beteg} = int(rand() * BETEG_NAPOK) + 1;
  }
   
  $adatok{nap} = 0;
  $adatok{oltasmutato} = 0;
  $adatok{oltottak} = 0;
  $adatok{osszeseset} = KEZDO_BETEG;
   
  $adatok{napi_ertekek} = [];

  while (covidCiklus(\%adatok) > 0 ) {
  }
  
  return %adatok;
}

my %eredmeny = covidSzimulacio(korlatozas_ciklus => 100, korlatozas_erosseg => 0.7);

my $ratioX = 320.0 / 320.0;

my $path = '';
my $x=0;
my $cmd = 'M';

for my $adat (@{$eredmeny{napi_ertekek}}) {
  my $y = 200 - ($adat->[0] / 100);
  
  $path .= $cmd . $x . " " . $y . " ";
  
  $cmd = 'L';
  $x += $ratioX;
}

my $svg = "<svg height=\"200\" width=\"320\">\n";
$svg .=   "    <path d=\"###PATH###\" style=\"stroke:rgb(0,0,255);stroke-width:2;fill:none;stroke-linejoin:round\" />\n";
$svg .=   "</svg>\n";

$svg =~ s/###PATH###/$path/;

print Dumper($eredmeny{osszeseset});

open( FH, ">", "covid.svg" ) or die "Can't open file for write: $!\n";
print FH $svg;
close(FH);



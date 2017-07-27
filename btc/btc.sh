#!/bin/bash

if [ "$#" -eq "0" ]
then
  COIN="BTC"
else
  COIN=$1
fi

COIN=${COIN^^}

price_eur() {
  python -c 'import json; import sys; print json.load(sys.stdin)["RAW"]["'$COIN'"]["EUR"]["PRICE"]'
}

price_usd() {
  python -c 'import json; import sys; print json.load(sys.stdin)["RAW"]["'$COIN'"]["USD"]["PRICE"]'
}

AMOUNT=${2:-1.0}

EUR=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=$COIN&tsyms=EUR" | price_eur)
CONTOS=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=$COIN&tsyms=EUR" | price_eur)
USD=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=$COIN&tsyms=USD" | price_usd)

EUR=$(echo "$EUR" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
USD=$(echo "$USD" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
CONTOS=$(echo "$CONTOS" "$AMOUNT" | awk '{ printf "%.2f\n", (($1 * $2)*200.482)/1000}')
CONTOSINT=${CONTOS%.*}
ESCUDOS=$(echo "$CONTOS" "$CONTOSINT" | awk '{ printf "%.3f\n", ($1 - $2)*1000}')
ESCUDOS=${ESCUDOS%.*}

if [ "$CONTOSINT" -ne "0" ]
then
  CONTOSSTR="$CONTOSINT Contos de rei"
fi

if [ "$ESCUDOS" -ne "0" ]
then
  if [ "$CONTOSINT" -ne "0" ]
  then
  ESCUDOSSTR=" e $ESCUDOS escudos"
  else
  ESCUDOSSTR="$ESCUDOS escudos"
  fi
fi
echo "$AMOUNT $COIN = $USD Usd   $AMOUNT $COIN = $EUR Eur   $AMOUNT $COIN = $CONTOSSTR$ESCUDOSSTR"

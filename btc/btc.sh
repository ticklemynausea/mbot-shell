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
USD=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=$COIN&tsyms=USD" | price_usd)

EUR=$(echo "$EUR" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
USD=$(echo "$USD" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')

echo "$AMOUNT $COIN = $USD usd   $AMOUNT $COIN = $EUR eur"

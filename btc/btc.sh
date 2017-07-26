#!/bin/bash

btce_price_eur() {
  python -c 'import json; import sys; print json.load(sys.stdin)["btc"]["eur"]["kraken"]["last"]'
}

btce_price_usd() {
  python -c 'import json; import sys; print json.load(sys.stdin)["btc"]["usd"]["bitfinex"]["last"]'
}

AMOUNT=${1:-1.0}

USD=$(curl -sf http://preev.com/pulse/units:btc+usd/sources:bitfinex | btce_price_usd)
EUR=$(curl -sf http://preev.com/pulse/units:btc+eur/sources:kraken | btce_price_eur)

USD=$(echo "$USD" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
EUR=$(echo "$EUR" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')

echo "$AMOUNT btc = $USD usd = $EUR eur"

#!/bin/bash

eth_price_eur() {
  python -c 'import json; import sys; print json.load(sys.stdin)["RAW"]["ETH"]["EUR"]["PRICE"]'
}

btc_price_eur() {
  python -c 'import json; import sys; print json.load(sys.stdin)["RAW"]["BTC"]["EUR"]["PRICE"]'
}

AMOUNT=${1:-1.0}

ETH=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=EUR" | eth_price_eur)
BTC=$(curl -sf "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=EUR" | btc_price_eur)

ETH=$(echo "$ETH" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
BTC=$(echo "$BTC" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')

echo "$AMOUNT ETH = $ETH eur \\ $AMOUNT BTC = $BTC eur"

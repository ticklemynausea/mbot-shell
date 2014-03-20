#!/bin/bash
 
btce_price() {
  python -c 'import json; import sys; print json.load(sys.stdin)["markets"]["btce"]["price"]'
}
 
AMOUNT=${1:-1.0}
 
USD=$(curl -sf http://preev.com/pulse/source:btce/unit:btc,usd | btce_price)
EUR=$(curl -sf http://preev.com/pulse/source:btce/unit:btc,eur | btce_price)
 
USD=$(echo "$USD" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
EUR=$(echo "$EUR" "$AMOUNT" | awk '{ printf "%.2f\n", $1 * $2}')
 
echo "$AMOUNT btc = $USD usd = $EUR eur"

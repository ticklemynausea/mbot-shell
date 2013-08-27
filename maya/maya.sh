#!/bin/bash
# maya.sh
# !maya [carneiro touro gemeos carangueijo leao virgem balanca escorpiao sagitario capricornio aquario peixes]

A=("carneiro" "touro" "gemeos" "carangueijo" "leao" "virgem" "balanca" "escorpiao" "sagitario" "capricornio" "aquario" "peixes")

I=${1//[^a-z]/}

S=1
for B in ${A[@]}
do
	if [ "$B" == "$I" ]
	then
		break
	fi
	((S++))
done

if [ $S -gt 12 ]
then
	echo "!maya ["${A[*]}"]"
	exit
fi

H="`curl -s http://www.cartasdamaya.pt/pt-pt/horoscopos | xml2`"

MAYATIT="`echo "$H" |
	awk -F '=' '/header\/h2\/a\/@title=/ {print $2;if (++c==1) exit}'`"

HORO="`echo "$H" |
	awk -F '=' 'BEGIN {s='$S'*2}
		/article\/(div\/){6}p\=/ {if (++c==s-1) h=$2; else if (c==s) print h" "$2 }'`"

echo "$MAYATIT" "$HORO"

#!/bin/bash
#
# cradits: http://orteil.dashnet.org/callmeshirley

A=( "slap" "fuck" "spank" "smack" "pinch" "rub" "mock" "squeeze" "suck" "bite" "bite off" "chew" "lick" "flap" "stroke" "touch" "smell" "sniff" "jizz on" "rub one out on" "wank to" "shit on" "piss on" "paint" "fist" "scratch" "screw" "kiss" "finger" "jiggle" "tickle" "hold" "grab" "blow on" "scream at" "befriend" "write a book about" "sue" "marry" "rape" "make love to" "pepper" "twist" "tenderize" "spit on" "fart on" "meet" "spend a charming afternoon with" "introduce your sister to" "sandwich" "write fanfic about" "blog about" "let's have a minute of silence for" "listen to" "google" "stick your dick in" "prance around in" "make your way inside" "plunder" "swiggity" "eat" "stuff" "hump" "humiliate" "blow" "blow up" "fancy" "berate" "rate" "rustle" )

B=( "tits" "ass" "dick" "mouth" "face" "balls" "cock" "crotch" "face" "beard" "moustache" "buns" "boobs" "boobies" "breasts" "chest" "butt" "buttocks" "nips" "nipples" "vag" "snatch" "cunt" "fanny" "skirt" "pants" "panties" "loins" "undies" "bra" "shorts" "jimmies" "crack" "thighs" "rump" "arse" "feet" "nuts" "cat" "horse" "goat" "dog" "parrot" "steak" "cheese" "hose" "goatee" "sideburns" "sandwich" "booty" "mother" "father" "grand-parents" "neighbor" "shiggity" "dinner" "shizzle" "bunny" "evil twin" "thing" "pickle" "nutsack" )

C=( "Shirley" "Sally" "Dolly" "Pedro" "Jose" "Juanita" "Sharon" "Geoffrey" "Susan" "Mary" "Stanley" "Bradley" "Barney" "Brandon" "Milford" "Robert" "Rosie" "Steve" "Patrick" "Jeffrey" "Brian" "David" "Santa" "Batman" "mommy" "daddy" "grandpa" "grandma" "auntie" "uncle" "pretty" "maybe" "when you're home" "when you're done" "darling" "fabulous" )


n_A=${#A[*]}
n_B=${#B[*]}
n_C=${#C[*]}


echo "Well ${A[$((RANDOM%n_A))]} my ${B[$((RANDOM%n_B))]} and call me ${C[$((RANDOM%n_C))]}."

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console

TIMEOUT = 5

def autoDeFe(processo, adcautelam=False):

    result = ""
    extra = "crime"
    shown = 0

    # Se for pesquisa, mostra o registo actual / total
    if adcautelam:
        result = "[%d/%d] " % (
            processo['next'] - 1 if processo['next'] else processo['total'],
            processo['total'])
        processo = processo['message']

    # Titulo
    result = "%s%s" % (result, processo['titulo'])

    # Quase todos têm crime
    if processo['crime']:
        result = "%s | Crime: %s" % (result, processo['crime'])
        shown = shown + 1
    # Se tiver sentença, nao printa mais dados sobre o processo (moar)
    if processo['sentenca']:
        result = u"%s | Sentença: %s" % (result, processo['sentenca'])
        shown = shown + 1

    if shown < 2:
        # Se tiver notas e outros dados
        if processo['notas'] and processo['outros']:
            # Ver qual deles é maior e printar
            if len(processo['notas']) > len(processo['outros']):
                result = "%s | Notas: %s" % (result, processo['notas'])
                extra = "notas"
            else:
                result = "%s | Outros dados: %s" % (result, processo['outros'])
                extra = "outros"
        # Senão printa as Notas
        elif processo['notas']:
            result = "%s | Notas: %s" % (result, processo['notas'])
            extra = "notas"
        # Ou os Outros dados
        elif processo['outros']:
            result = "%s | Outros dados: %s" % (result, processo['outros'])
            extra = "outros"

    # Se for pesquisa
    if adcautelam:
        # Verifica se o match é o mesmo de algum dos items printados
        # Tou a comparar duas vezes com o crime quando o "extra" não é definido
        if (processo['crime'] != processo['match']['value'] and
                processo['sentenca'] != processo['match']['value'] and
                processo[extra] != processo['match']['value']):

            # Printa o match
            result = "%s | %s: %s" % (
                result,
                processo['match']['key'],
                processo['match']['value'])

    # Adiciona o short url
    result = "%s | %s" % (result, processo['url'])

    return result

def degredo():
    request = requests.get('https://inquisicao.deadbsd.org/api/degredo', timeout=TIMEOUT)

    j = request.json()
    result = autoDeFe(j)
    print_console(result)

def adcautelam(key, page):
    request = requests.get('https://inquisicao.deadbsd.org/api/adcautelam?key=' + key + '&page=' + str(page), timeout=TIMEOUT)

    if request.status_code == 404:
        print_console("Not found")
    else:
        j = request.json()
        result = autoDeFe(j, adcautelam=True)
        print_console(result)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        degredo()
    if len(sys.argv) > 1:
        ARGS = ' '.join(sys.argv[1:])

        KEY = False
        PAGE = 1

        MATCH = re.search(r"^(?P<key>.*?)(?P<page> \d+)?$", ARGS)
        if MATCH.group('key'):
            KEY = MATCH.group('key')
        if MATCH.group('page'):
            PAGE = int(MATCH.group('page').strip())

        if KEY:
            adcautelam(KEY, PAGE)

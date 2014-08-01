# coding=utf8
#!/usr/bin/env python

"""
.tr [form(default:auto)] <to> <texto>
.tr sem args: halp
"""
from common import api_request, langs
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mylib


def help():
  mylib.print_console(".tr [from] <to> <text>")
  mylib.print_console("languages: " + " ".join(langs))

def parse_args():
  args = sys.argv[1:]
  l = len(args)

  if l < 2 :
    help()
    exit(0)

  input_lang = args[0]

  if input_lang not in langs:
    help()
    exit(0)

  output_lang = args[1]
  if output_lang not in langs:
    output_lang = input_lang
    input_lang = "auto"
    args = " ".join(args[1:])
  else:
    args = " ".join(args[2:])

  return (input_lang, output_lang, args)



def output(output_lang, result):
  mylib.print_console("\002[%s>%s]\002 %s" % (result[2], output_lang, result[0][0][0]))

def main():
  (input_lang, output_lang, args) = parse_args()
  result = api_request(input_lang, output_lang, args)
  output(output_lang, result);
  
if __name__=="__main__":
  main()

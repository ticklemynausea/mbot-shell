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
  mylib.print_console(".tr <l1,l2,l3,...,ln> <text>")
  mylib.print_console("languages: " + " ".join(langs))

def parse_args():
  args = sys.argv[1:]
  l = len(args)

  if l < 2 :
    help()
    exit(0)

  lang_sequence = args[0].split(",")
  text = " ".join(args[1:])
  
  #print lang_sequence
  #print text
  #exit(0)

  for input_lang in lang_sequence:
    if input_lang not in langs:
      help()
      exit(0)

  return (lang_sequence, text)



def output(output_lang, result):
  mylib.print_console("\002[%s>%s]\002 %s" % (result[2], output_lang, result[0][0][0]))

def main():
  (lang_sequence, text) = parse_args()
  
  input_lang = lang_sequence[0]
  for output_lang in lang_sequence[1:]:
    result = api_request(input_lang, output_lang, text)
    output(output_lang, result);
    input_lang = output_lang
  
if __name__=="__main__":
  main()
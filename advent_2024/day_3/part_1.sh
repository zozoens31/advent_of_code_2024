#!/bin/bash

grep -oP 'mul\(\d{1,3},\d{1,3}\)' $1 --color=none | xargs python -c 'import sys
def mul(a,b):
  return a*b

print(sum(eval(arg) for arg in sys.argv[1:]))'
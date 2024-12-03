#!/bin/bash

grep -oP "(mul\(\d{1,3},\d{1,3}\))|(do(n't)?\(\))" $1 --color=none |
    sed s"/don't/dont/" |
    xargs python -c 'import sys
enabled = [True]

def do():
  enabled.clear()
  enabled.append(True)
  return 0

def dont():
  enabled.clear()
  enabled.append(False)
  return 0

def mul(a,b):
  return a*b if enabled[0] else 0

print(sum(eval(arg) for arg in sys.argv[1:]))'
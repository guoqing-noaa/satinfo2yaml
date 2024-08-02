#!/usr/bin/env python
import yaml
import sys

args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"Usage: {args[0]} <file>")
  exit()

myfile=args[1]
with open(myfile) as stream:
  #print(yaml.load(stream,Loader=yaml.UnsafeLoader))
  print(yaml.safe_load(stream))

#!/usr/bin/env python
import yaml
import sys

def traverse(subdata,n): # traverse the yaml dict tree until reaching leafs
  if isinstance(subdata,dict):
    n=n+1
    for key,value in subdata.items():
      print(f"{' '*n*3}{key}")
      traverse(value,n)

def getFinalValue(subdata,keytree): # get the value for a hirearchy key string
  if keytree: # not empty
    subdata=subdata[keytree.pop(0)]
    if not keytree: # if empty now
      return subdata
    else:
      return getFinalValue(subdata,keytree)

# ====== main =========
args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"Usage: {args[0]} <file> [keystr] [traverse|dump|changeto='']")
  exit()
myfile=args[1]
mykeystr=""
if nargs >1:
  mykeystr=args[2]

with open(myfile) as yfile:
  data=yaml.safe_load(yfile)

# list the top-level keys
for key in data.keys():
  print(f"{key}")

if mykeystr:
  print(f"\n=== {mykeystr} ==")
  keytree=mykeystr.split("/")
  print(getFinalValue(data,keytree))
  exit()
  
  subdata=data.get(mykeystr)
  traverse(subdata,1)
  exit()
  if isinstance(subdata,dict):
    for key in subdata.keys():
      print(key)
    print(f"==== subdata ======")
    yaml.dump(subdata, sys.stdout)

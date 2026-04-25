#!/usr/bin/env python3
import sys,re

if len(sys.argv)==3:
    findkey=sys.argv[1]
    word=sys.argv[2]
    keys=re.findall(findkey,word)
    print(len(keys))
else:
    print("none")
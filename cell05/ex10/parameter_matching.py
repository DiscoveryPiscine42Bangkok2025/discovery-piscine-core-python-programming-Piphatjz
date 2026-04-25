#!/usr/bin/env python3
import sys

if len(sys.argv)==2:
    pw=input("What was the parameter? ")
    if pw == sys.argv[1]:
        print("Good job!")
    else:
        print("Nope, sorry...")
else:
    print("none")
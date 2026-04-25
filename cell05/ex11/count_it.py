#!/usr/bin/env python3
import sys
if len(sys.argv)>1:
    par=len(sys.argv)-1
    print(f"parameters: {par}")
    ar=sys.argv[1:]
    for i in ar:
        print(f"{i}: {len(i)}")
else:
    print("none")

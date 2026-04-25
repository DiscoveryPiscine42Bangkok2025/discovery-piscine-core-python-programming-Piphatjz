#!/usr/bin/env python3
import sys
if len(sys.argv) == 2:
    ar=sys.argv[1]
    for i in ar:
        if i =='z':
            print("z",end="")
    print()
else:
    print("none")
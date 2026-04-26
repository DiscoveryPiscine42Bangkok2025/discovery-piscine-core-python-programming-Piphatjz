#!/usr/bin/env python3
import sys

def shrink(a):
    return print(a[:8])
def enlarge(a):
    return print(a+'Z'*(8-len(a)))

if len(sys.argv) >1:
    ar=sys.argv[1:]
    for i in ar:
        if len(i)<8:
            enlarge(i)
        elif len(i) > 8:
            
            shrink(i)
        else:
            print(i)
else:
    print("none")
#!/usr/bin/env python3

import sys

if len(sys.argv)==3:
    f=int(sys.argv[1])
    s=int(sys.argv[2])
    ar=list(range(f,s+1))
    print(ar)
else:
    print("none")
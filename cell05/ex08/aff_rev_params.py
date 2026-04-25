#!/usr/bin/env python3
import sys 
if len(sys.argv)>1:
    a=sys.argv[1:]
    for i in a:
        print(f"{i}")
    # print(sys.argv[1:])
else:
    print("none")
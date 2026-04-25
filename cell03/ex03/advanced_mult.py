#!/usr/bin/env python3

import sys

if len(sys.argv)>1 and  not sys.argv[1].isdigit():
    print("none")
    sys.exit()

i=0
while i<=10:
    print(f"Table de {i}:", end=" ")
    j=0
    while j<=10:
        print(f"{j*i}", end=" ")
        j+=1
    i+=1
    print("")
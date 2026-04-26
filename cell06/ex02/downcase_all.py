#!/usr/bin/env python3
import sys
def downcase_it(text):
    return text.lower()

if len(sys.argv)>1:
    ar=sys.argv[1:]
    for i in ar:
        print(downcase_it(i))
else:
    print("none")
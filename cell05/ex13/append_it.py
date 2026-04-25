#!/usr/bin/env python3
import sys
if len(sys.argv)>1:
    word=sys.argv[1:]
    for i in word:
        match i:
            case i:
                if i.endswith("ism"):
                    pass
                else:
                    print(i+"ism")

else:
    print("none")
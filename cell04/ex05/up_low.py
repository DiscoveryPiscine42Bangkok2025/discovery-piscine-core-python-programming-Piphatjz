#!/usr/bin/env python3

text=str(input(""))
for i in range(0,len(text)):
    if text[i].isupper():
            m=text[i]
            m=m.lower()
            print(m,end="")
    else:
            m=text[i]
            m=m.upper()
            print(m,end="")

print()
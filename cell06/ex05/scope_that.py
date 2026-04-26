#!/usr/bin/env python3

def add_one(x):
    x = x + 1
    print("Inside function:", x)


num = 5
print("Before:", num)

add_one(num)

print("After:", num)
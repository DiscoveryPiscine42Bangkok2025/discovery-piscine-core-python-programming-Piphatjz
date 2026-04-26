#!/usr/bin/env python3

def greetings(name=None):
    if name == None:
        return print("Hello, noble stranger.")
    if isinstance(name,str):
        return print(f"Hello, {name}.")
    else:
        return print("Error! It was not a name.")

greetings('Alexandra')
greetings('Wil')
greetings()
greetings(42)
#!/usr/bin/env python3

def array_of_names(d):
    result = []
    for first, last in d.items():
        full_name = first.capitalize() + " " + last.capitalize()
        result.append(full_name)
    return result

persons = {
    "jean": "valjean",
    "grace": "hopper",
    "xavier": "niel",
    "fifi": "brindacier"
}

print(array_of_names(persons))
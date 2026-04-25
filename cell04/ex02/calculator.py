#!/usr/bin/env python3

num1=int(input("Give me the first number: "))
num2=int(input("Give me the second number: "))
print("Thank you!")

sum=[("+",num1+num2),("-",num1-num2),("/",num1//num2),("*",num1*num2)]
for op,result in sum:
    print(f"{num1} {op} {num2} = {result}")

import sys
import random
from api.tools import mult

print("hello world",mult(10,20))
print(sys.version)

#the end parameter replaces the new line with a new end character, end= is the parameter.
print("hello world",end=", ")
print("this will print on the same line")

#this will separate each parameter with a space
print("multiple items",40,"separated by commas in the print statement")

#casting data types because in python there isn't any 
x = str(3)
y = int(3)
z = float(3)

print("Different cast results",x,y,z)
print("Prove the types:","x",type(x),"y",type(y),"z",type(z))

#creating mutliple assigns at once
x,y,z = "orange","banana","cherry"
print(x,y,z)

#or one value can be assigned to multiple variables
x=y=z = "orange"
print(x,y,z)

#unpacking when a list or tuple has multiple values in it
fruits = ["apple","banana","cherry"]
x,y,z = fruits
print(x,y,z)

#variable scoping
x = "awesome"
def myfunc():
    print("python is " + x)

myfunc()

x = 5
print("The value of x changed from string to int",x)

#global keyword inside functions to promote a var globally

def myfuncglob():
    global myglob 
    myglob = "fantastic"

myfuncglob()
print("python is:",myglob)

#random number usage with the import of the random package

print(random.randrange(1,10))

#STRINGS STRINGS STRINGS
astring = "the best things in life are free!"
print("free" in astring)

if "free" in astring:
    print("free was found in the string astring")

mystring = "*halo*"
mystring = mystring.replace("*","/")
print(mystring)
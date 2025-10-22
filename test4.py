res = "python"
r = ""
# concatenation(+)
'''for c in res: 
    r = r +c
print(r)
repitation (*)
print(res*6) # pythonpythonpythonpythonpythonpython
print(res*-2) # empty string
# print(res*1.2) -- error can't multiply sequence by non-int of type 'float' 
'''
# string comparision
#unicode is used instead of ascii
print("gate" == "gate")
print("Gate" == "gate")
print("Gate" != "Gate")
print("Gate" >= "Gate")
print("Gate" <= "Gate")
print("Gate" < "Gate")
print("Gate" < "gate")
print("Gate" > "gate")
print("Gate" > "Gate")
# Membership operator[in ,not in]
print('p' in res)
print("p" in res)
print('pth' in res)
#escape sequence character
str1 = "today's match is between \"india and england\" "
print(str1)
print('today\'s match is between " india and england " ')
print("hello \n world")
print("hello\b world \b")
print("\141")
print("\1412")
print("\141\142")
print("\x65")
print("\x61")
# string formatting[%s,%d,%f]
name = "john"
marks = 90 
print("hello %s your marks is %d"%(name,marks))
print("hello %s your marks is %f"%(name,marks))

print("hello {} your marks is {}".format(name,marks))
print("hello {0} your marks is {1}".format(name,marks))
print("hello {0} your marks is{0}".format(name,marks))
print("hello {age} your marks is {name} ".format(name = "ravi",age = 69))
# f -string
mane = "vari"
age = 69
print(f"my name is {mane} , age is {age}")
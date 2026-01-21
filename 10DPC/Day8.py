#Function:
def sum(a,b):
    return(int(a+b))
def diff(a,b):
    return(int(a-b))
def product(a,b):
    return(int(a*b))
def divide(a,b):
    return(int(a/b))
num1=int(input("enter first number: "))
num2=int(input("enter second number: "))
Fset={'add','sub','multiply','divide'}
F1=frozenset(Fset)
print("Select one opertion from below list")
for i in F1:
    print(i)
oper=input("enter operation: ")

if oper == 'add':
    print(sum(num1,num2))
elif oper == 'sub':
    print(diff(num1,num2))
elif oper == 'multiply':
    print(product(num1,num2))
elif oper == 'divide':
    print(divide(num1,num2))
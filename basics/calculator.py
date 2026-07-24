# Calculator App
a= int(input("Enter the First number:"))
b= int(input("Enter the Second number:"))
print("The value of a+b is:", a+b)
print("The value of a-b is:", a-b)
print("The value of a*b is:", a*b)
print("The value of a/b is:", a/b)
print("The value of a//b is:", a//b)
print("The value of a%b is:", a%b)
print("The value of a**b is:", a**b)

# Using match-case
x = int(input("Enter the value of x:"))
y = int(input("Enter the value of y:"))
operator = input("Enter operator:")
match operator:
    case '+':
        print("The value of x+y is:", x+y)
    case '-':
        print("The value of x-y is:", x-y)
    case '*':
        print("The value of x*y is:", x*y)
    case '/':
        ("The value of x/y is:", x/y)
    case _:
        print("Invalid operator")
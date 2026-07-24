#Grading system
# marks= [ 10,20,30,40,50,60,70,80,90,100]
# x = int(input("Enter your marks:"))
# if (x >= 100):
#     print("Grade A")
# elif (x < 100 and x >=80):
#     print("Grade B")
# elif (x <80 and x >= 60):
#     print("Grade C")
# elif (x <60 and x >=40):
#     print("Grade D")
# else:
#     print("Fail")

#Using Function
def marks():
    # marks = [10,20,30,40,50,60,70,80,90,100]
    x = int(input("Enter your marks:"))
    if (x == 100):
        print("Grade A")
    elif (x < 100 and x>=75):
        print("Grade B")
    elif (x < 75 and x >=40):
        print("Grade C")
    else:
        print("Fail")
marks()


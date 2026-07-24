questions = [
    [
        "What is the capital of India?", "Mumbai", "Delhi", "Kolkata", "Chennai", 2
    ],
    [   
        "Who is known as the Father of Computers?", "Charles Babbage", "Newton", "Einstein", "Tesla", 1
    ],
    [
        "Which is a programming language?", "Python", "Snake", "Lion", "Tiger", 1
    ],
    [
        "Which language was used to create fb?", "Python", "French", "Javascript", "Php", 4
    
    ],
    [
        "What is the full form of CPU?", "Central Process Unit", "Central Processing Unit", "Computer Processing Unit" , "Control Processing Unit", 2
    ],
    [
        "Which device is used to type?", "Mouse", "Keyboard", "Monitor", "Printer", 2
    ],
    [
        "Which of the following is a python data type?", "integer", "real", "number", "digit", 1
    ],
    [
        "What is the correct file extension for Python?", ".pt", ".py", ".pyt", ".python", 2
    ],
    [
        "Which keyword is used to define a function in Python?", "function", "define", "def", "fun", 3
    ],
    [
        "Which of the following is mutable", "Tuple", "String", "List", "Integer", 3
    ]
]
levels = [1000,2000,3000,5000,10000,20000,40000,80000,160000,320000]
money = 0
for i in range(0, len(questions)):
    question = questions[i]
    print(f"\n\nQuestion for Rs. {levels[i]}")
    print(f"a. {question[1]} b. {question[2]}")
    print(f"c. {question[3]} d. {question[4]}")
    reply = int(input("Enter your answer (1-4) or 0 to quit"))
    if(reply == 0):
        money = levels[i-1]
        break

    if(reply == question[-1]):
        print(f"Correct answer, you have won Rs. {levels[i]}")
        if(i == 4):
            money = 10000
        elif(i == 9):
            money = 320000
        elif(i == 14):
            money = 10000000
    else:
        print("Wrong answer!")
        break

print(f"You take home money is{money}")


    

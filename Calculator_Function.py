print('''Select Operation.
1. Add
2. Subtract
3. Multiply
4. Divide
5. Exponent
6. Modulus
7. Smaller of two
8. Greater of two
9. Average of two
''')
ask_user = 'c'
while ask_user == "c":
    choice = float(raw_input("Enter an operation number [1-9]: "))
    number1 = float(raw_input("Enter the first Number: "))
    number2 = float(raw_input("Enter the second Number: "))
    if (choice == 1):
        print(number1+number2)
    elif ( choice == 2):
        print(number1-number2)
    elif ( choice == 4):
        print(number1/number2)
    elif (choice == 3):
        print(number1*number2)
    elif (choice == 6):
        print(number1%number2)
    elif (choice == 5):
        print(number1**number2)
    elif (choice == 9):
        print((number1+number2)/2.0)
    elif (choice == 7):
        if (number1 < number2):
            print ("The smaller number is:", number1)
        else:
            print ("The smaller number is", number2)
    elif (choice == 8):
        if (number1 > number2):
            print ("The bigger number is:", number1)
        else:
            print ("The bigger number is", number2)
    else:
        print("Please Enter a valid choice between 1-9")
        
    ask_user = raw_input("Press q to quit and c to continue: ")
print("End of program")
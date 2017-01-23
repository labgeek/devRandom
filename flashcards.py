# this program uses three extra libraries
import sys
import math
import random

print("Welcome!")
print("In this program you can practice your multiplication facts!")

# this "print" statement makes a blank line (it looks nicer)
print

# these are called "variables".  A variable is a word that stands for a number
# the number that a variable represents can be changed later in the program
response = 0
answer = 0
right = 0
wrong = 0


# this command makes the program run over and over again in a "loop"
while 1:

    # these commands create two variables that are random numbers
    a = random.randint(1, 12)
    b = random.randint(1, 12)

    # this command calculates what the answer should be
    answer = a * b

    print("What is " + str(a) + " * " + str(b) + "?")

    # the "raw_input" command lets the user guess the answer
    response = raw_input('Answer: ')

    # this command will exit the program if the user types "quit"
    if response == "quit":
        break

    # this command will show the user how they're doing
    elif response == "stats":
        print("You have answered " + str(right) + " right out of " +
              str(right + wrong) + ".")

    # these lines say what should happen if the user guesses right
    elif int(answer) == int(response):
        print("Correct!")
        right = right + 1

    # these lines say what should happen if the user guesses wrong   
    else:
        print("Wrong")
        wrong = wrong + 1

    print

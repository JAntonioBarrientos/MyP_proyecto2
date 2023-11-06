import sys

player = input("I want your age: \n")
age = int(player)

if age < 18:
    sys.exit("You are too young to play this game.")
else:
    print("Welcome to the game!")
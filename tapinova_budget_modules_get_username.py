# Olga Tapinova
# olga.tapinova@weizmann.ac.il


import sys


def get_username():

    if len(sys.argv) > 2:
        print(
            f"""
Invalid input. Usage: 
    {sys.argv[0]} 
or
    {sys.argv[0]} NAME (without spaces)
"""
        )
        exit()

    if len(sys.argv) == 2:
        username = sys.argv[1]
    else:
        while True:
            username = input("What is your name? ")
            check = username.split(" ")
            if len(check) == 1:  # if ' ', '!', ';' in username -> regex; ../
                break
            print("Invalid input! Use '_' instead of space")

    return username.lower()

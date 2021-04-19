# Olga Tapinova
# olga.tapinova@weizmann.ac.il


def change_currency():

    while True:
        currency = input("Input new currency: ").lower()
        check = currency.split(" ")

        if len(check) == 1:
            print(f"Current currency is '{currency}'")
            return currency

        print(f"Invalid input {currency}! Use '_' instead of space")
        _ = input("Press enter to continue!\n")

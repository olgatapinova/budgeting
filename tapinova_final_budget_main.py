# Olga Tapinova
# olga.tapinova@weizmann.ac.il


import warnings
from tapinova_budget_modules_get_username import get_username
from tapinova_budget_modules_add_item import add_data
from tapinova_budget_modules_edit_item import edit_item
from tapinova_budget_modules_change_currency import change_currency
from tapinova_budget_modules_statistics_basic import show_stat_check_file


def main():
    warnings.filterwarnings("ignore")

    username = get_username()
    currency = "nis"
    print(f"\nHi, {username}\nCurrent currency is '{currency}'")

    while True:
        choice = input(
            f"""
Select:
    'a' to add new expenses or incomes
    'e' to edit existing data
    's' to show the statistics
    'c' to change the currency
    'x' to exit\n"""
        )
        if choice.lower() == "x":
            exit("Bye!")
        elif choice.lower() == "a":
            add_data(username + "_" + currency)
        elif choice.lower() == "e":
            edit_item(username + "_" + currency)
        elif choice.lower() == "s":
            show_stat_check_file(username + "_" + currency)
        elif choice.lower() == "c":
            currency = change_currency()
        else:
            print(f"'{choice}' is not in the list. Try again!")
        input("Press enter to continue!\n")              # function


main()

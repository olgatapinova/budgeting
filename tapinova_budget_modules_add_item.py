# Olga Tapinova
# olga.tapinova@weizmann.ac.il


import os
from datetime import date
import re
import pandas as pd


def file_exists(filename):

    return os.path.isfile(filename)


def is_int(val):

    try:
        num = int(val)
    except ValueError:
        return False
    return True


def is_float(val):

    try:
        num = float(val)
    except ValueError:
        return False
    return True


def get_item():

    while True:
        choice = input(
            f"""
Select:
    1. to add an income
    2. to add an expense
"""
        )
        if choice.lower() == "1":
            item = "income"
            break
        elif choice.lower() == "2":
            item = "expense"
            break
        else:
            print(f"'{choice}' is not in the list. Try again!")

    return item


def check_month_day_year(month, day, year):

    months_days = {
        "01": 31,
        "02": 28,
        "03": 31,
        "04": 30,
        "05": 31,
        "06": 30,
        "07": 31,
        "08": 31,
        "09": 30,
        "10": 31,
        "11": 30,
        "12": 31,
    }

    # datetime does not work for years before 1971
    if int(year) < 1971:
        return False

    # accept Feb 29
    if (int(year) % 4 == 0 and int(year) % 100 != 0) or (int(year) % 400 == 0):
        months_days["02"] = 29

    # check month and day
    if int(month) == 0 or int(month) > 12:
        return False
    if int(day) == 0 or int(day) > months_days[month]:
        return False
    return True


def find_date_in_string_regex(choice):

    match = re.search(r"(\A(\d\d\d\d)[-./]?(\d\d)[-./]?(\d\d)\Z)", choice)  # see date function
    if match:
        if check_month_day_year(match.group(3), match.group(4), match.group(2)):
            new_date = date(
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
            )
            return new_date
    else:
        return False


def get_date():

    while True:
        today_date = date.today()
        choice = input(
            f"""
Select:
    't' to use today's date: {today_date}
    or print the date you want starting from 1971-01-01:
    'yyyy-mm-dd'/'yyyy.mm.dd'/'yyyy/mm/dd'/'yyyymmdd'
"""
        )

        if choice.lower() == "t":
            return today_date
        else:
            new_date = find_date_in_string_regex(choice)
            if new_date:
                return new_date
        print(f"Wrong input '{choice}', try again!")
        _ = input("Press enter to continue!\n")


def get_category_from_list(categories):

    if len(categories) == 0:
        print("The list of categories is empty!")
        return None

    string_categories = "\n".join(
        [f"    {i + 1}. {cat}" for i, cat in enumerate(categories)]
    )

    while True:
        choice = input(
            f"""
Select one of the existing categories:
{string_categories}
or 'n' type another one.
"""
        )
        if choice == "n":
            return None

        if is_int(choice):
            num_category = int(choice)
            if num_category <= 0 or num_category > len(categories):
                print("Wrong input (not in the range), try again!")
                continue
            category = categories[num_category - 1]
            return category.lower()

        elif is_float(choice):
            print("Wrong input (not integer), try again!")
        else:
            print(f"Invalid input '{choice}', try again!")


def get_category_from_file(filename, item):

    category = None

    if file_exists(filename):
        df = pd.read_csv(filename)
        dt_item = df[df["item"] == item]
        categories = list(set(dt_item["category"]))
        category = get_category_from_list(categories)  # can be false for empty list

    if not category:
        category = input("Type a category: ")

    return category.lower()


def get_amount():

    while True:
        amount = input("Type amount of money: ")

        if is_int(amount):
            amount = int(amount)
        elif is_float(amount):
            amount = float(amount)
        else:
            print("Not a number, try again!")
            continue

        if amount >= 0:
            return amount
        else:
            print("Negative value!")


def get_comment():
    comment = input("Type a comment if you want: ")
    return comment


def add_line_to_file(
    username, item_date, item, item_category, item_amount, item_comment
):

    filename = username + ".csv"
    line = f'{str(item_date)},{item},"{item_category}",{str(item_amount)},"{item_comment}"\n'

    if file_exists(filename):
        with open(filename, "a") as out:
            out.write(line)
    else:
        with open(filename, "w") as out:
            out.write("date,item,category,amount,comment\n")
            out.write(line)

    return


def sort_data_in_file(username):

    filename = username + ".csv"
    df_sorted = pd.read_csv(filename).sort_values(by=["date"])
    df_sorted.to_csv(filename, index=False)
    return


def add_data(username):

    print(f"Here we add the data, {username}")
    filename = username + ".csv"

    item = get_item()
    item_date = get_date()
    item_category = get_category_from_file(filename, item)
    item_amount = get_amount()
    item_comment = get_comment()

    add_line_to_file(
        username, item_date, item, item_category, item_amount, item_comment
    )
    sort_data_in_file(username)

# Olga Tapinova
# olga.tapinova@weizmann.ac.il


import pandas as pd
from tapinova_budget_modules_add_item import (
    is_int,
    get_item,
    get_amount,
    get_date,
    get_category_from_file,
    get_comment,
    file_exists,
)


def read_csv_to_df_with_dates(filename):

    df = pd.read_csv(filename)  # automatically?
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def get_item_to_edit(df):

    if len(df) == 0:
        print("The list is empty!")
        return df

    while True:
        item = get_item()

        if item in list(df.item):
            df_chosen = df[df.item == item].copy()
            print(f"Now there are only {item}s in the list")
            return df_chosen
        else:
            print(f"There is no {item}s in the file. Show the entire data to check")
            return df


def get_first_last_days_in_df(df):

    first_day = df.iloc[0]["date"]
    last_day = df.iloc[len(df.date) - 1]["date"]
    print(f"The period is from {first_day} to {last_day}")
    return first_day, last_day


def get_date_with_limits(first_day, last_day):

    while True:
        new_date = get_date()

        if first_day <= new_date <= last_day:
            return new_date
        else:
            print(f"Invalid input. Choose a day between {first_day} and {last_day}")
        _ = input("Press enter to continue!\n")


def get_date_to_edit(df):

    if len(df) == 0:
        print("The list is empty!")
        return df

    while True:
        first_day, last_day = get_first_last_days_in_df(df)
        _ = input("Press enter to continue!\n")

        dat = get_date_with_limits(first_day, last_day)

        if dat in list(df.date):
            df_chosen = df[df.date == dat].copy()
            print(f"Now there are only items with the date {dat}")
            return df_chosen
        else:
            print("No such date in the list! Show the entire data to check")
            return df


def get_amount_to_edit(df):

    if len(df) == 0:
        print("The list is empty!")
        return df

    while True:
        amount = get_amount()
        if amount in list(df.amount):
            df_chosen = df[df.amount == amount].copy()
            print(f"Now there are only items with the amount of money {amount}")
            return df_chosen
        else:
            print("No such amount in the list. Show the entire data to check!")
            return df


def pick_up_row_from_filtered_data(df):

    if len(df) == 0:
        print("The list is empty!")
        return df

    while True:
        print(df)
        choice = input("Select index from the list: ")

        if is_int(choice):
            ind = int(choice)
            if ind in df.index:
                df_row = df[df.index == ind]
                print(f"\nYou chose:\n{df_row}")
                return df_row
            else:
                print("Not in the list, try again")
        else:
            print("Not an integer, try again")
        _ = input("Press enter to continue!\n")


def choose_data_row_to_edit(df):

    df_chosen = df.copy()

    while True:
        choice = input(
            """
Select number to filter the data by the following criteria:
    1. to choose only incomes/expenses
    2. to choose the date
    3. to choose the amount of money

    4. to show the data with chosen parameters
    5. clear the parameters to start again (load the original data)

    6. to pick up a row from the filtered data
"""
        )

        if choice == "1":
            df_chosen = get_item_to_edit(df_chosen)
        elif choice == "2":
            df_chosen = get_date_to_edit(df_chosen)
        elif choice == "3":
            df_chosen = get_amount_to_edit(df_chosen)
        elif choice == "4":
            print(df_chosen)
        elif choice == "5":
            df_chosen = df.copy()
            print("You loaded the original data from the file.")
        elif choice == "6":
            df_chosen = pick_up_row_from_filtered_data(df_chosen)
            break
        else:
            print("Invalid input, try again!")

        _ = input("Press enter to continue!\n")
    return df_chosen


def get_new_data_to_edit(username):

    print("\nNow please, add new data instead of what you chose")
    filename = username + ".csv"
    _ = input("Press enter to continue!\n")

    item = get_item()
    item_date = get_date()
    item_category = get_category_from_file(filename, item)
    item_amount = get_amount()
    item_comment = get_comment()

    return [item_date, item, item_category, item_amount, item_comment]


def edit_df_with_new_row(df, row_chosen, new_data):

    new_df = df.copy()

    new_df[
        (new_df.date == row_chosen.iloc[0]["date"])
        & (new_df.item == row_chosen.iloc[0]["item"])
        & (new_df.category == row_chosen.iloc[0]["category"])
        & (new_df.amount == row_chosen.iloc[0]["amount"])
        & (new_df.comment == row_chosen.iloc[0]["comment"])
    ] = new_data

    return new_df


def edit_item(username):

    filename = username + ".csv"
    if not file_exists(filename):
        print("There is no file for this name and currency. Please, add new data")
        return

    df_file = read_csv_to_df_with_dates(filename)
    if len(df_file) == 0:
        print("The file is empty. Add new data")
        return

    row_chosen = choose_data_row_to_edit(df_file)  # still data frame
    new_data = get_new_data_to_edit(username)
    new_df = edit_df_with_new_row(df_file, row_chosen, new_data)

    df_sorted = new_df.sort_values(by=["date"])
    df_sorted.to_csv(filename, index=False)
    return

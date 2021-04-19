# Olga Tapinova
# olga.tapinova@weizmann.ac.il


import pandas as pd
import matplotlib.pyplot as plt
from tapinova_budget_modules_add_item import get_category_from_file


def plot_bars_grouped_df(dfmy, item, ax):

    if len(dfmy) == 0:
        print(f"No data for {item}s. Cannot plot a bar graph")
        return

    dfmy.plot.bar(ax=ax, legend=False)
    ax.set_title(f"{item} by months")
    ax.set(xlabel="months", ylabel="amount")

    ticks = [f"{el[0]}-{el[1]}" for el in dfmy.index]
    ax.set_xticklabels(ticks, rotation=45)

    return


def plot_dynamics_short_df(df, item, ax):

    if len(df):
        dfdt = df.copy()
        dfdt["date"] = pd.to_datetime(
            dfdt["date"]
        )  # for .date() there is no index.year, index.month
        dfdt.index = dfdt["date"]
        dfmy = dfdt.groupby([dfdt.index.year, dfdt.index.month]).sum()

        plot_bars_grouped_df(dfmy, item, ax)
    else:
        print(f"No data for {item}s. Cannot plot the distribution by month")
    return dfmy


def show_dynamics_by_category(filename, df, item):

    categories = list(set(df[df.item == item].category))
    if not categories:
        print(f"No data for {item}s")
        return

    category = get_category_from_file(filename, item)

    if not category or (category not in categories):
        print(f"No data in {item}s for this category")
        return

    df_short = df[(df.item == item) & (df.category == category)][["date", "amount"]]
    if len(df_short):
        fig, ax = plt.subplots(1, figsize=(12, 8))
        plot_dynamics_short_df(df_short, category, ax)
        print("Close the figure window to continue")
        plt.show()
    else:
        print(f"No data with such parameters: {item}, {category}!")
    return


def show_dynamics_by_month(df):

    if len(df):
        df_income = df[df.item == "income"][["date", "amount"]]
        df_expense = df[df.item == "expense"][["date", "amount"]]

        flag = ""
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        if len(df_income):
            df_income_grouped = plot_dynamics_short_df(df_income, "income", axs[0])
            flag += "i"
        else:
            print(f"No data for income")
        if len(df_expense):
            df_expense_grouped = plot_dynamics_short_df(df_expense, "expense", axs[1])
            flag += "e"
        else:
            print(f"No data for expense")

        if flag == "i":
            df_rem = df_income_grouped
        elif flag == "e":
            df_rem = -df_expense_grouped
        elif flag == "ie":
            df_rem = df_income_grouped - df_expense_grouped

        plot_bars_grouped_df(df_rem, "remainder", axs[2])

        plt.tight_layout(pad=2.0, w_pad=0.5, h_pad=1.0)
        print("Close the figure window to continue")
        plt.show()
    else:
        print("No data in the file!")
    return


def choose_dynamics_to_show(filename, df):

    while True:
        choice = input(
            """
Select to show the dynamics:
    1. by category for incomes
    2. by category for expenses
    3. for incomes, expenses and remainders
    'x' to return to the previous menu
"""
        )
        if choice == "1":
            show_dynamics_by_category(filename, df, "income")
        elif choice == "2":
            show_dynamics_by_category(filename, df, "expense")
        elif choice == "3":
            show_dynamics_by_month(df)
        elif choice.lower() == "x":
            return
        else:
            print("Invalid input, try again!")

        _ = input("Press enter to continue!\n")

# Olga Tapinova
# olga.tapinova@weizmann.ac.il


from datetime import date
import matplotlib.pyplot as plt
from tapinova_budget_modules_add_item import file_exists
from tapinova_budget_modules_edit_item import read_csv_to_df_with_dates, get_date_with_limits, get_first_last_days_in_df
from tapinova_budget_modules_statistics_dynamics import choose_dynamics_to_show


def choose_time_period(first_day, last_day):

    while True:
        print("Input the starting point")
        start_t = get_date_with_limits(first_day, last_day)
        _ = input("Press enter to continue!\n")

        print("Input the last day")
        end_t = get_date_with_limits(first_day, last_day)

        start_t = date(start_t.year, start_t.month, start_t.day)
        end_t = date(end_t.year, end_t.month, end_t.day)

        if start_t <= end_t:
            return start_t, end_t
        else:
            print(f"Invalid input. Change the order of the dates: {start_t}, {end_t}!")
        _ = input("Press enter to continue!\n")


def cut_df_by_period(df):

    if len(df):
        first_day, last_day = get_first_last_days_in_df(df)
        _ = input("Press enter to continue!\n")

        start_t, end_t = choose_time_period(first_day, last_day)

        new_df = df[df.date.between(start_t, end_t)]
        return new_df
    else:
        return df


def plot_by_category_pie(df, item, ax):

    df_short = df[df.item == item][["category", "amount"]]

    if len(df_short):
        categories = list(set(df_short.category))
        cat_amount = [0] * len(categories)
        for ind, cat in enumerate(categories):
            cat_amount[ind] = sum(df_short[df_short.category == cat].amount)

        ax.pie(cat_amount, labels=categories, autopct="%1.1f%%")
        ax.set_title(f"Total {item}s: {sum(cat_amount)}")
    else:
        print(f"No data for {item}s. Cannot plot a pie chart")
    return


def plot_items_by_dates(df, item, ax):

    df_short = df[df.item == item][["date", "amount"]]
    if len(df_short):
        dates = sorted(list(set(df_short.date)))
        amounts = [0] * len(dates)

        for ind, day in enumerate(dates):
            dates[ind] = dates[ind]
            amounts[ind] = df_short[df_short.date == day].amount.sum()

        ax.bar(dates, amounts)
        ax.set_title(f"Daily {item}")
        ax.set(xlabel="dates", ylabel="amount")

    else:
        print(f"No data for {item}s. Cannot plot the daily distribution")
    return


def get_statistics_from_df_over_period(df):

    if len(df):
        _, _ = get_first_last_days_in_df(df)

        total_income = sum(df[df.item == "income"].amount)
        print(f"Total incomes is {total_income}")

        total_expenses = sum(df[df.item == "expense"].amount)
        print(f"Total expenses is {total_expenses}")

        total_rem = total_income - total_expenses
        print(f"The remainder by the end of the period is {total_rem}")

        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        plot_by_category_pie(df, "income", axs[0, 0])
        plot_items_by_dates(df, "income", axs[0, 1])
        plot_by_category_pie(df, "expense", axs[1, 0])
        plot_items_by_dates(df, "expense", axs[1, 1])

        plt.tight_layout(pad=2.0, w_pad=0.5, h_pad=1.0)
        print("Close the figure window to continue")
        plt.show()
    else:
        print(f"No data!")
    return


def choose_basic_statistics_dynamics(filename):

    df = read_csv_to_df_with_dates(filename)
    while True:
        choice = input(
            """
Select:
    1. to show statistics over the entire data
    2. to choose a period to show
    3. to show the dynamics
    'x' to return to the main menu
"""
        )
        if choice == "1":
            get_statistics_from_df_over_period(df)
        elif choice == "2":
            df_part = cut_df_by_period(df)
            get_statistics_from_df_over_period(df_part)
        elif choice == "3":
            choose_dynamics_to_show(filename, df)
        elif choice.lower() == "x":
            return
        else:
            print("Invalid input, try again!")
        _ = input("Press enter to continue!\n")


def show_stat_check_file(username):
    print(f"Here we show the statistics, {username}")
    filename = username + ".csv"
    if file_exists(filename):
        choose_basic_statistics_dynamics(filename)
    else:
        print("The file is empty. Please, add new data")
    return

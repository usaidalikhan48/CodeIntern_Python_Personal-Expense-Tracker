import csv
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

FILE_NAME = "expenses.csv"


def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Amount", "Category", "Description"])
    except FileExistsError:
        pass

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food, Travel, etc.): ")
    description = input("Enter description: ")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date == "":
        date = datetime.date.today().strftime("%Y-%m-%d")

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, description])

    print(" Expense added successfully")


def read_expenses():
    expenses = []
    with open(FILE_NAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            expenses.append(row)
    return expenses


def summary(period):
    expenses = read_expenses()
    today = datetime.date.today()
    total = 0

    for e in expenses:
        e_date = datetime.datetime.strptime(e["Date"], "%Y-%m-%d").date()

        if period == "daily" and e_date == today:
            total += e["Amount"]
        elif period == "weekly" and (today - e_date).days <= 7:
            total += e["Amount"]
        elif period == "monthly" and e_date.month == today.month:
            total += e["Amount"]

    print(f"💰 {period.capitalize()} Expense: ₹{total}")


def top_categories():
    expenses = read_expenses()
    category_total = defaultdict(float)

    for e in expenses:
        category_total[e["Category"]] += e["Amount"]

    print("\n Top Spending Categories:")
    for cat, amt in sorted(category_total.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat}: ₹{amt}")

    return category_total


def visualize():
    category_total = top_categories()

    categories = list(category_total.keys())
    amounts = list(category_total.values())

    plt.figure(figsize=(10,4))

    
    plt.subplot(1,2,1)
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xticks(rotation=45)

    
    plt.subplot(1,2,2)
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expense Distribution")

    plt.tight_layout()
    plt.show()


def menu():
    init_file()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. Daily Summary")
        print("3. Weekly Summary")
        print("4. Monthly Summary")
        print("5. View Top Categories")
        print("6. Visualize Expenses")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            summary("daily")
        elif choice == "3":
            summary("weekly")
        elif choice == "4":
            summary("monthly")
        elif choice == "5":
            top_categories()
        elif choice == "6":
            visualize()
        elif choice == "7":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice")

menu()

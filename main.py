import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

monthly_budget = 5000

from datetime import datetime

# Store expenses here for now
expenses = []

def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date == "":
        date = datetime.today().strftime('%Y-%m-%d')

    category = input("Enter category (e.g. Food, Transport): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }

    with open("expenses.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print("✅ Expense added successfully!")

def view_expenses():
    print("\n=== Saved Expenses ===")
    try:
        print("Saving to:", os.path.abspath("expenses.csv"))

        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"Date: {row[0]}, Category: {row[1]}, Amount: {row[2]}, Description: {row[3]}")
    except FileNotFoundError:
        print("No expenses recorded yet.")

def check_budget():
    total = 0
    current_month = datetime.today().strftime('%Y-%m')

    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                expense_date = row[0]
                if expense_date.startswith(current_month):
                    total += float(row[2])
        print(f"\n📆 Monthly total so far: R{total:.2f}")
        print(f"💸 Budget limit: R{monthly_budget:.2f}")

        if total > monthly_budget:
            print("🚨 ALERT: You have exceeded your monthly budget!")
        else:
            print("✅ You're within your budget.")
    except FileNotFoundError:
        print("No expenses found.")

def show_expense_chart():
    categories = defaultdict(float)

    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[1]
                amount = float(row[2])
                categories[category] += amount

        if not categories:
            print("No expenses to display.")
            return

        # Plot
        plt.figure(figsize=(8, 5))
        plt.bar(categories.keys(), categories.values(), color='skyblue')
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount Spent")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No expenses found.")

from datetime import datetime

def show_monthly_trends():
    monthly_totals = defaultdict(float)

    try:
        with open("expenses.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                date_str = row[0]
                amount = float(row[2])

                # Convert string date to datetime object
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                month_name = date_obj.strftime("%b")  # Short month name like Jan, Feb, etc.
                month_key = date_obj.strftime("%Y-%m")  # Keep this for sorting

                monthly_totals[month_key] += amount  # Use YYYY-MM for sorting

        if not monthly_totals:
            print("No expenses to display.")
            return

        # Sort and map to short month names
        sorted_keys = sorted(monthly_totals.keys())
        totals = [monthly_totals[key] for key in sorted_keys]
        month_labels = [datetime.strptime(key, "%Y-%m").strftime("%b") for key in sorted_keys]

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(month_labels, totals, marker='o', color='purple')
        plt.title("Monthly Expense Trends")
        plt.xlabel("Month")
        plt.ylabel("Total Spent (R)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No expenses found.")


def show_menu():
    print("\n=== Expense Tracker Menu ===")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Check Budget Limit")
    print("4. Show Expense Graph")
    print("5. Show Monthly Trends")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            check_budget()
        elif choice == '4':
            show_expense_chart()
        elif choice == '5':
            show_monthly_trends()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()


import os
import json
from tabulate import tabulate

# File to store expenses
EXPENSES_FILE = 'expenses.json'

# Load expenses from file
def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    return []

# Save expenses to file
def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense
def add_expense():
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    
    expenses = load_expenses()
    expenses.append({
        "description": description,
        "amount": amount,
        "category": category
    })
    save_expenses(expenses)
    print("Expense added successfully!")

# View all expenses
def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    
    table = [[i+1, e['description'], e['amount'], e['category']] for i, e in enumerate(expenses)]
    print(tabulate(table, headers=["ID", "Description", "Amount", "Category"], tablefmt="grid"))

# Delete an expense
def delete_expense():
    view_expenses()
    expenses = load_expenses()
    
    if not expenses:
        return
    
    expense_id = int(input("Enter the ID of the expense to delete: ")) - 1
    if 0 <= expense_id < len(expenses):
        expenses.pop(expense_id)
        save_expenses(expenses)
        print("Expense deleted successfully!")
    else:
        print("Invalid ID.")

# Main menu
def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

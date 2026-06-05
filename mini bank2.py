def create_account():
    name = input("Enter the name of account holder: ").strip()
    while not name:
        print("Name cannot be empty. Please enter a valid name.")
        name = input("Enter the name of account holder: ").strip()

    print(f"Welcome, {name}! Your mini bank account is ready.")
    return {
        "name": name,
        "balance": 0.0,
        "history": []
    }


def add_history(account, message):
    account["history"].append(message)


def deposit(account):
    try:
        amount = float(input("Enter the amount to deposit: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount > 0:
        account["balance"] += amount
        add_history(account, f"Deposit: +${amount:,.2f}")
        print(f"${amount:,.2f} deposited successfully.")
    else:
        print("Invalid amount. Deposit must be greater than zero.")


def withdraw(account):
    try:
        amount = float(input("Enter the amount to withdraw: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Invalid amount. Withdrawal must be greater than zero.")
    elif amount > account["balance"]:
        print("Insufficient balance.")
    else:
        account["balance"] -= amount
        add_history(account, f"Withdrawal: -${amount:,.2f}")
        print(f"${amount:,.2f} withdrawn successfully.")


def display_balance(account):
    print(f"Current balance for {account['name']}: ${account['balance']:,.2f}")


def display_history(account):
    print(f"\nTransaction history for {account['name']}:")
    if account["history"]:
        for item in account["history"]:
            print(" - ", item)
    else:
        print(" No transactions yet.")


def display_menu():
    print("\n=========== Mini Bank System ===========")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Display balance")
    print("4. Transaction history")
    print("5. Exit")


def prompt_choice():
    try:
        return int(input("Enter your choice: ").strip())
    except ValueError:
        return None


account = create_account()
while True:
    display_menu()
    choice = prompt_choice()

    if choice == 1:
        deposit(account)
    elif choice == 2:
        withdraw(account)
    elif choice == 3:
        display_balance(account)
    elif choice == 4:
        display_history(account)
    elif choice == 5:
        print("Thank you for using the mini bank!")
        break
    else:
        print("Invalid choice. Please try again.")

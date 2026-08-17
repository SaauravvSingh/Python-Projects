# ==========================================
#              MINI ATM MACHINE
# ==========================================

# Account Information
account = {
    "name": "Saurav",
    "account_no": "1234567890",
    "balance": 100000,
    "pin": 4321,
    "type": "Personal Account"
}

# Another account for Money Transfer
other_accounts = {
    "9876543210": {
        "name": "Rahul",
        "balance": 50000
    }
}

# ==========================================
#          ATM SETTINGS / LIMITS
# ==========================================
MAX_WITHDRAWAL = 20000
DAILY_WITHDRAWAL_LIMIT = 50000
daily_withdrawal = 0
transaction_history = []
transaction_id = 1000

# ==========================================
#        FUNCTION: TRANSACTION ID
# ==========================================
def generate_transaction_id():
    global transaction_id
    transaction_id += 1
    return "TXN" + str(transaction_id)

# ==========================================
#        FUNCTION: MINI STATEMENT
# ==========================================
def mini_statement():
    print("\n================================")
    print("         MINI STATEMENT")
    print("================================")
    if len(transaction_history) == 0:
        print("No transactions yet.")
    else:
        for transaction in transaction_history:
            print(transaction)
    print("--------------------------------")
    print("Current Balance:", account["balance"])
    print("================================")

# ==========================================
#        FUNCTION: TRANSACTION HISTORY
# ==========================================
def show_transaction_history():
    print("\n================================")
    print("       TRANSACTION HISTORY")
    print("================================")
    if len(transaction_history) == 0:
        print("No transactions found.")
    else:
        for transaction in transaction_history:
            print(transaction)
    print("================================")

# ==========================================
#             MINI ATM
# ==========================================
print("================================")
print("          === MINI ATM ===")
print("================================")

# ==========================================
#        PIN LOGIN - 3 ATTEMPTS
# ==========================================
attempts = 3
login_success = False

while attempts > 0:
    pin = input("Enter Your PIN: ")
    if pin.isdigit():
        pin = int(pin)
    else:
        print("PIN must contain numbers only.")
        attempts -= 1
        print("Attempts remaining:", attempts)
        continue

    if pin == account["pin"]:
        login_success = True
        print("\nLogin Successful!")
        break
    else:
        attempts -= 1
        print("Invalid PIN!")
        if attempts > 0:
            print("Attempts remaining:", attempts)
        else:
            print("\n================================")
            print("       ACCOUNT LOCKED!")
            print("================================")
            print("Too many incorrect PIN attempts.")
            print("Please contact the bank.")

# ==========================================
#        IF LOGIN SUCCESSFUL
# ==========================================
if login_success:
    while True:
        print("\n================================")
        print("           ATM MENU")
        print("================================")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Account Details")
        print("5. Change PIN")
        print("6. Mini Statement")
        print("7. Transaction History")
        print("8. Transfer Money")
        print("9. Exit")
        print("================================")
        choice = input("Enter your choice: ")

        # ==================================
        #       1. CHECK BALANCE
        # ==================================
        if choice == "1":
            print("\n--------------------------------")
            print("Your Balance is:", account["balance"])
            print("--------------------------------")

        # ==================================
        #       2. DEPOSIT MONEY
        # ==================================
        elif choice == "2":
            amount = float(input("Enter amount to deposit: ₹"))
            # Deposit Validation
            if amount <= 0:
                print("\nInvalid Amount!")
                print("Deposit amount must be greater than 0.")
            else:
                account["balance"] = account["balance"] + amount
                txn_id = generate_transaction_id()
                transaction_history.append(
                    txn_id + " | Deposit | +₹" + str(amount)
                )
                print("\n================================")
                print("Money Deposited Successfully!")
                print("Amount:", amount)
                print("New Balance:", account["balance"])
                print("Transaction ID:", txn_id)
                print("================================")

        # ==================================
        #       3. WITHDRAW MONEY
        # ==================================
        elif choice == "3":
            amount = float(input("Enter amount to withdraw: ₹"))
            # Withdrawal Validation
            if amount <= 0:
                print("\nInvalid Amount!")
                print("Withdrawal amount must be greater than 0.")
            # Maximum withdrawal per transaction
            elif amount > MAX_WITHDRAWAL:
                print("\nWithdrawal Failed!")
                print("Maximum withdrawal per transaction is ₹", MAX_WITHDRAWAL)
            # Daily withdrawal limit
            elif daily_withdrawal + amount > DAILY_WITHDRAWAL_LIMIT:
                remaining_limit = DAILY_WITHDRAWAL_LIMIT - daily_withdrawal
                print("\nDaily Withdrawal Limit Exceeded!")
                print("You can withdraw only ₹", remaining_limit, "more today.")
            # Insufficient Balance
            elif amount > account["balance"]:
                print("\nInsufficient Balance!")
            else:
                account["balance"] = account["balance"] - amount
                daily_withdrawal = daily_withdrawal + amount
                txn_id = generate_transaction_id()
                transaction_history.append(
                    txn_id + " | Withdrawal | -₹" + str(amount)
                )
                print("\n================================")
                print("Money Withdrawn Successfully!")
                print("Amount:", amount)
                print("Remaining Balance:", account["balance"])
                print("Transaction ID:", txn_id)
                print("================================")
                # Receipt
                print("\n================================")
                print("             RECEIPT")
                print("================================")
                print("Account Name :", account["name"])
                print("Transaction  : Withdrawal")
                print("Amount       : ₹", amount)
                print("Transaction ID:", txn_id)
                print("Balance      : ₹", account["balance"])
                print("Status       : Successful")
                print("================================")

        # ==================================
        #       4. ACCOUNT DETAILS
        # ==================================
        elif choice == "4":
            # Mask account number
            masked_account_no = "XXXXXX" + account["account_no"][-4:]
            print("\n================================")
            print("        ACCOUNT DETAILS")
            print("================================")
            print("Name          :", account["name"])
            print("Account No.   :", masked_account_no)
            print("Account Type  :", account["type"])
            print("Balance       : ₹", account["balance"])
            print("================================")

        # ==================================
        #       5. CHANGE PIN
        # ==================================
        elif choice == "5":
            print("\n================================")
            print("           CHANGE PIN")
            print("================================")
            old_pin = input("Enter your current PIN: ")
            if old_pin.isdigit():
                old_pin = int(old_pin)
                if old_pin == account["pin"]:
                    new_pin = input("Enter your new 4-digit PIN: ")
                    confirm_pin = input("Confirm your new PIN: ")
                    if new_pin.isdigit() and len(new_pin) == 4 and confirm_pin.isdigit():
                        if new_pin == confirm_pin:
                            account["pin"] = int(new_pin)
                            print("\nPIN changed successfully!")
                        else:
                            print("\nNew PINs do not match.")
                    else:
                        print("\nPIN must contain exactly 4 digits.")
                else:
                    print("\nIncorrect current PIN.")
            else:
                print("\nInvalid PIN.")

        # ==================================
        #       6. MINI STATEMENT
        # ==================================
        elif choice == "6":
            mini_statement()

        # ==================================
        #       7. TRANSACTION HISTORY
        # ==================================
        elif choice == "7":
            show_transaction_history()

        # ==================================
        #       8. TRANSFER MONEY
        # ==================================
        elif choice == "8":
            print("\n================================")
            print("          MONEY TRANSFER")
            print("================================")
            recipient_account = input("Enter recipient account number: ")
            if recipient_account == account["account_no"]:
                print("\nYou cannot transfer money to your own account.")
            elif recipient_account not in other_accounts:
                print("\nRecipient account not found.")
            else:
                amount = float(input("Enter amount to transfer: ₹"))
                if amount <= 0:
                    print("\nInvalid Amount!")
                    print("Transfer amount must be greater than 0.")
                elif amount > account["balance"]:
                    print("\nInsufficient Balance!")
                else:
                    # Deduct money from our account
                    account["balance"] = account["balance"] - amount
                    # Add money to recipient
                    other_accounts[recipient_account]["balance"] += amount
                    txn_id = generate_transaction_id()
                    transaction_history.append(
                        txn_id + " | Transfer to " +
                        other_accounts[recipient_account]["name"] +
                        " | -₹" + str(amount)
                    )
                    print("\n================================")
                    print("Transfer Successful!")
                    print("================================")
                    print("Recipient :", other_accounts[recipient_account]["name"])
                    print("Amount    : ₹", amount)
                    print("Transaction ID:", txn_id)
                    print("New Balance : ₹", account["balance"])
                    print("================================")
                    # Transfer Receipt
                    print("\n================================")
                    print("          TRANSFER RECEIPT")
                    print("================================")
                    print("From       :", account["name"])
                    print("To         :", other_accounts[recipient_account]["name"])
                    print("Amount     : ₹", amount)
                    print("Transaction:", txn_id)
                    print("Balance    : ₹", account["balance"])
                    print("Status     : Successful")
                    print("================================")

        # ==================================
        #       9. EXIT
        # ==================================
        elif choice == "9":
            print("\n================================")
            print("   Thank You for Using Mini ATM")
            print("================================")
            print("Please take your card.")
            print("Have a nice day!")
            break

        # ==================================
        #       INVALID CHOICE
        # ==================================
        else:
            print("\nInvalid Choice!")
            print("Please select a number from 1 to 9.")
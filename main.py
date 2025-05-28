from models import User, Loan
from db import create_tables

def menu():
    print("""
1. Register
2. Login
3. Exit
""")
    return input("Choose an option: ")

def user_menu():
    print("""
1. Make an Apply
2. Make Payment
3. Check Balance
4. View Payment History
5. Logout
""")
    return input("Choose an option: ")

def main():
    create_tables()
    current_user = None

    while True:
        if not current_user:
            choice = menu()
            if choice == '1':
                username = input("Username: ")
                password = input("Password: ")
                user = User.register(username, password)
                if user:
                    print("Registered successfully.")
                else:
                    print("Username already exists.")
            elif choice == '2':
                username = input("Username: ")
                password = input("Password: ")
                user = User.login(username, password)
                if user:
                    print("Login successful.")
                    current_user = user
                else:
                    print("Invalid credentials.")
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
        else:
            user_id = current_user.get_id()
            loan = Loan(user_id)
            choice = user_menu()
            if choice == '1':
                amount = float(input("Enter loan amount: "))
                loan.apply(amount)
                print("Loan applied successfully.")
            elif choice == '2':
                payment = float(input("Enter payment amount: "))
                loan.pay(payment)
                print("Payment successful.")
            elif choice == '3':
                balance = loan.check_balance()
                print(f"Outstanding Balance: {balance}")
            elif choice == '4':
                history = loan.view_payments()
                print("Payment History:", history)
            elif choice == '5':
                current_user = None
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()

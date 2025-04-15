# Main options that user is greeted to
def main_options():
    print("\n--------------------\n1: Create an Account\n\n2: Access Your Account\n\n3: Exit\n--------------------\n")
    try:
        choice = int(input("Type a number 1-3: "))
    except ValueError:
        choice = 0
    while int(choice) <1 or int(choice)>3:
        print("Make sure you enter a number from 1-3: ")
        options()
    if choice == 1:
        create_account()
    elif choice == 2:
        access_account()
    elif choice == 3:
        # Allows user to terminate program easily
        exit()

# Options that will be displayed after option 2 is chosen in the previous menu and user signs in to their account
def account_options():
    print("\n--------------------\n1: Check Your Balance\n\n2: Deposit Money\n\n3: Withdraw Money\n\n4: Modify Account\n\n5: Delete Account\n\n6: Exit\n--------------------\n")
    try:
        choice = int(input("Type a number 1-6: "))
    except ValueError:
        choice = 0
    while int(choice) <1 or int(choice)>6:
        print("Make sure you enter a number from 1-6: ")
        options()
    if choice == 1:
        check_balance()
    elif choice == 2:
        deposit()
    elif choice == 3:
        withdraw()
    elif choice == 4:
        modify_account()
    elif choice == 5:
        delete_account()
    elif choice == 6:
        # Allows user to terminate program easily
        exit()

# Greeting Message
print("Hello, welcome to Yusuf's Bank! Here are your options:")
main_options()
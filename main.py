# from tkinter import *
# from tkinter import ttk
# import mysql.connector

# root = Tk()
# root.title("Banking App")

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# ttk.Button(mainframe, text='Create Account', command=)


import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'elite_102', password = 'rA911msA!')

cursor = connection.cursor()

account_id = 0

#Main options that user is greeted to
def main_options():
    while True:
        print("\n--------------------\n1: Create an Account\n\n2: Access Your Account\n\n3: Exit\n--------------------\n")
        try:
            choice = int(input("Type a number 1-3: "))
        except ValueError:
            choice = 0

        if choice == 1:
            create_account()
        elif choice == 2:
            access_account()
        elif choice == 3:
            exit()
        else:
            print("Make sure you enter a number from 1-3.")


# Options that will be displayed after option 2 is chosen in the previous menu and user signs in to their account
def account_options():
    while True:
        print("\n--------------------\n1: Check Your Balance\n\n2: Deposit Money\n\n3: Withdraw Money\n\n4: Modify Account\n\n5: Delete Account\n\n6: Exit\n--------------------\n")
        try:
            choice = int(input("Type a number 1-6: "))
        except ValueError:
            choice = 0

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
            exit()
        else:
            print("Make sure you enter a number from 1-6.")


def create_account():
    global usernames
    # Makes sure username is not repeated
    username = input("Enter a username: ").upper()
    while username in usernames:
        username = input("\n\nUsername is already taken\nEnter another username: ")
    
    password = input("Enter a password: ")
    first_name = input("Enter your first name: ").upper()
    last_name = input("Enter your last name: ").upper()
    pin = ""
    while len(pin) != 4:
        try:
            pin=input("Enter a 4-digit PIN: ")
            int(pin)
        except ValueError:
            pin = ""
        if len(pin) !=4:
            print("Make sure to enter a PIN that contains only integers and is 4 digits")
    # Insert info into mySQL database
    addData = "INSERT INTO user_info (username, password, first_name, last_name, PIN, balance) VALUES (%s, %s, %s, %s, %s, 0)"
    cursor.execute(addData, (username, password, first_name, last_name, pin))
    connection.commit()

    print("Account Created!\n\nPlease sign in to access your account")
    access_account()


def access_account():
    global account_id
    username = input("\nEnter your username: ").upper() 
    password = input ("Enter your password: ")

    findAccount = "SELECT user_id, first_name, last_name FROM user_info WHERE username = %s AND password = %s"
    cursor.execute(findAccount, (username, password))
    result = cursor.fetchone()
    if result:
        account_id = result[0]
        print(f"\nWelcome back, {result[1]} {result[2]}!")
        account_options()
    else:
        retry = input("\nIncorrect username or password\nWould you like to try again? (y/n): ").lower()
        if retry == 'y':
            access_account()
        else:
            main_options()

def check_balance():
    global account_id
    cursor.execute("SELECT balance FROM user_info WHERE user_id = %s", (account_id,))
    result = cursor.fetchone()
    if result:
        print(f"\nYour current balance is: ${result[0]:.2f}")
    else:
        print("Could not retrieve your balance.")

def deposit():
    global account_id
    while True:
        deposit_amount = input("\nEnter the amount you want to deposit (up to 2 decimal places): ")
        if '.' in deposit_amount:
            integer_part, decimal_part = deposit_amount.split('.', 1)
            if len(decimal_part) > 2:
                print("You can only enter up to two digits after the decimal point. Try again.")
                continue

        try:
            deposit_amount = float(deposit_amount)
            cursor.execute("UPDATE user_info SET balance = balance + %s WHERE user_id = %s", (deposit_amount, account_id))
            connection.commit()
            print(f"\nSuccessfully deposited ${deposit_amount:.2f}.")
            check_balance()
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
def withdraw():
    global account_id
    cursor.execute("SELECT PIN, balance FROM user_info WHERE user_id = %s", (account_id,))
    result = cursor.fetchone()
    while True:
        pin = input("Enter your 4-digit PIN: ")
        if pin == result[0]:
            withdrawal_amount = input("How much would you like to withdraw? ")
            if '.' in withdrawal_amount:
                integer_part, decimal_part = withdrawal_amount.split('.', 1)
                if len(decimal_part) > 2:
                    print("You can only enter up to two digits after the decimal point. Try again.")
                    continue
            try:
                withdrawal_amount=float(withdrawal_amount)
                if float(withdrawal_amount) > result[1]:
                    print("Make sure you do not withdraw more than your account balance. Try Again")
                    continue
                cursor.execute("UPDATE user_info SET balance = balance - %s WHERE user_id = %s", (withdrawal_amount, account_id))
                connection.commit()
                print(f"\nSuccessfully withdrew ${withdrawal_amount:.2f}.")
                check_balance()
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
        else:
            print("Invalid PIN. Try again")

def modify_account():
    global account_id
    global usernames
    cursor.execute("SELECT username, password, first_name, last_name FROM user_info WHERE user_id = %s", (account_id,))
    result = cursor.fetchone()
    print(f"\nUsername: {result[0]}\nPassword: {result[1]}\nFirst Name: {result[2]}\nLast Name: {result[3]}")
    while True:
        print("\nChoose what to modify:\n--------------------\n1: Modify Username\n\n2: Modify Password\n\n3: Modify First Name\n\n4: Modify Last Name\n\n5: Done\n--------------------\n")
        try:
            choice = int(input("Type a number 1-5: "))
        except ValueError:
            choice = 0
            
        if choice == 1:
            usernames.remove(result[0])
            changed_element = input("Enter a username: ").upper()
            while changed_element in usernames:
                changed_element = input("\n\nUsername is already taken\nEnter another username: ")
            modified_column = "username"
        elif choice == 2:
            changed_element = input("Enter a new password: ")
            modified_column = "password"
        elif choice == 3:
            changed_element = input("Enter your First Name: ").upper()
            modified_column = "first_name"
        elif choice == 4:
            changed_element = input("Enter your Last Name: ").upper()
            modified_column = "last_name"
        elif choice == 5:
            break
        else:
            print("Make sure you enter a number from 1-5.")
        query = f"UPDATE user_info SET {modified_column} = %s WHERE user_id = %s"
        cursor.execute(query, (changed_element, account_id))
        connection.commit()

def delete_account():
    global account_id
    cursor.execute("SELECT PIN FROM user_info WHERE user_id = %s", (account_id,))
    result = cursor.fetchone()
    confirmation = input("Are you sure you want to delete your account (y/n): ").lower()
    if confirmation == 'y':
        while True:
            pin = input("Enter your 4-digit PIN. Enter '0' to quit: ")
            if pin == result[0]:
                cursor.execute("DELETE FROM user_info WHERE user_id = %s", (account_id,))
                connection.commit()
                main_options()
            elif pin == '0':
                break
            else:
                print("Incorrect PIN or invalid answer. Try again")
    



# Obtain all usernames to eliminate duplicates
usernames = []
cursor.execute("SELECT username FROM user_info")
usernames = [item[0] for item in cursor.fetchall()]

# Greeting Message
print("Hello, welcome to Yusuf's Bank! Here are your options:")
main_options()



cursor.close()
connection.close()
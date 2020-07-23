# import cursor as cursor
import pyodbc
import sys

global var_UID

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    'Database=LegoStore;'
    'Trusted_Connection=yes;'

)

cursor = conn.cursor()


# function to read from specified table


def read(table_name):
    # print("Read")
    cursor = conn.cursor()
    cursor.execute("Select * FROM " + table_name)
    for row in cursor:
        print(row)
        # print(f'row = {row}')
    print()


# read('login')


def login(conn):
    exist = input("Are you an existing customer? (y/n): ")
    if exist.lower() == "n":
        newCustomer(conn)
        read(conn)
    else:
        while True:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            cursor = conn.cursor()
            find_user = "SELECT * FROM login WHERE username = ? AND password = ?"
            cursor.execute(find_user, [username, password])
            results = cursor.fetchall()

            if results:
                for row in results:
                    print("Welcome " + row[0])
                    # global var_UID
                    var_UID = int(row[0])
                    print(var_UID)
                    return "exit"
            else:
                print("Username and password not recognized")


# login(conn)

def newCustomer(conn):
    # get username and password from new customer
    found = 0
    while found == 0:
        username = input("Please enter a username: ")
        cursor = conn.cursor()
        findUser = "SELECT * FROM login WHERE username = ?"
        cursor.execute(findUser, [username])

        if cursor.fetchall():
            print("Username is Taken. Please try again.")
        else:
            found = 1
    password = input("Please enter your password: ")
    password1 = input("Please reenter your password: ")
    while password != password1:
        print("Your passwords don't match. Please try again.")
        password = input("Please enter your password: ")
        password1 = input("Please reenter your password: ")
    insertData = '''INSERT INTO login(username,password) 
                    VALUES (?,?,?)'''
    cursor.execute(insertData, [username, password])
    conn.commit()
    # set id to be used to access the correct customer
    var_UID = int(conn.execute("SELECT @@IDENTITY as id").fetchone()[0])
    print(var_UID)

    print("Your new account was created.")
    print("Please fill out your customer profile.")

    # get info to fill out customer profile
    f_name = input('Please enter your first name: ')
    l_name = input('Please enter your last name: ')
    email = input('Please enter your email: ')
    phone = input('Please enter your phone number: ')
    address = input('Please enter your address: ')
    # still haven't gotten store_preference
    insertData = ('INSERT INTO customerInfo(customer_id, f_name, l_name, email, phone, address, username, password) \n'
                  '                        VALUES (?,?,?,?,?,?,?,?)')
    cursor.execute(insertData, [var_UID, f_name, l_name, email, phone, address, username, password])


def browse():
    choice = input("Would you like to browse by Bricks or by Sets?: ")
    if choice.lower() == "bricks":
        cursor = conn.cursor()
        cursor.execute("Select * FROM bricks")
        # cursor.execute("Select quantity, part_num, description, price FROM bricks")
        for row in cursor:
            # self note: add column names
            print(row[1], row[0], row[2], row[3])

    elif choice.lower() == "sets":
        cursor = conn.cursor()
        cursor.execute("Select name, quantity FROM brick_sets")
        for row in cursor:
            # self note: add column names and get price from bricks table
            print(row[0], row[1])


def search():
    choice = input("Would you like to search by Bricks or by Sets?: ")


# browse()


def emp_menu():
    print("1. Sale")
    print("2. Manage")
    print("3. Profile")
    print("x. Exit")
    function = input("Function: ")
    if function == "x":
        main_menu()



def main_menu():
    print("---------- Application Menu ----------")
    print("1.   Employee")
    print("2.   Customer")
    print("x.   Exit")
    choice = input("Application: ")
    print(choice)
    if choice == "1":
        emp_menu()
    elif choice == "2":
        login(conn)
        newCustomer(conn)
    elif choice == "x":
        sys.exit()


main_menu()

conn.close()

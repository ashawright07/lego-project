# import cursor as cursor
import numpy
import pyodbc
import sys
from datetime import date

# global var_UID
cart = numpy.empty((0, 5), str)
order_date = date.today()

conn = pyodbc.connect(
    'Driver={SQL Server};'
    # 'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
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


def emp_login():
    while True:

        username = input("username: ")
        password = input("password: ")
        cursor = conn.cursor()
        find_employee = "SELECT * FROM employee_login WHERE username = ? AND password = ?"
        cursor.execute(find_employee, [username, password])
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Welcome " + row[0])
                return "exit"
        else:
            print("Username and/or password not recognized")


def login(conn):
    exist = input("Are you an existing customer? (y/n): ")
    if exist.lower() == "n":
        newCustomer(conn)
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
                    print("Welcome " + row[1] + "!")
                    global var_UID
                    var_UID = int(row[0])  # global var_UID
                    print(var_UID)
                    return "exit"
            else:
                print("Username and password not recognized")


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
                    VALUES (?,?)'''
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
    conn.commit()


def browse():
    choice = input("Would you like to browse by Bricks or by Sets?: ")
    if choice.lower() == "bricks":
        cursor = conn.cursor()
        cursor.execute("Select * FROM bricks")
        # cursor.execute("Select quantity, part_num, description, price FROM bricks")
        print("%-10s %-10s %-20s %s" % ("Quantity", "Part Num", "Description", "Price"))
        for row in cursor:
            print("%-10s %-10s %-20s %s" % (row[1], row[0], row[2], row[3]))

    elif choice.lower() == "sets":
        cursor = conn.cursor()
        cursor.execute("SELECT a.quantity, a.name, b.price FROM brick_sets a "
                       "INNER JOIN (SELECT brick_set_parts.set_id, SUM(bricks.price) as price FROM bricks "
                       "INNER JOIN brick_set_parts ON bricks.part_num = brick_set_parts.part_num "
                       "GROUP BY brick_set_parts.set_id) b "
                       "ON a.set_id = b.set_id")
        print("%-10s %-15s %s" % ("Quantity", "Name", "Price"))
        for row in cursor:
            print("%-10s %-15s %s" % (row[0], row[1], row[2]))


def search():
    choice = input("Enter keyword to search: ")
    cursor = conn.cursor()
    cursor.execute("Select * FROM bricks Where part_num LIKE  '%" + choice +
                   "%' OR description LIKE  '%" + choice + "%' ")
    print("Brick Results")
    print("%-10s %-10s %-20s %s" % ("Quantity", "Part Num", "Description", "Price"))
    for row in cursor:
        print("%-10s %-10s %-20s %s" % (row[1], row[0], row[2], row[3]))

    cursor.execute("SELECT a.quantity, a.name, b.price FROM brick_sets a "
                   "INNER JOIN (SELECT brick_set_parts.set_id, SUM(bricks.price) as price FROM bricks "
                   "INNER JOIN brick_set_parts ON bricks.part_num = brick_set_parts.part_num "
                   "GROUP BY brick_set_parts.set_id) b "
                   "ON a.set_id = b.set_id WHERE a.name LIKE '%s%%' OR b.price LIKE '%s%%' " % (choice, choice))
    print("\nBrick Set Results")
    print("%-10s %-15s %s" % ("Quantity", "Name", "Price"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))


def addToCart():
    # find item
    global cart
    found = 0
    while found == 0:
        item = input("Enter the item you would like to add to your cart: ")

        cursor = conn.cursor()
        findItem = "SELECT * FROM bricks WHERE part_num = ?"
        cursor.execute(findItem, [item])
        results1 = cursor.fetchall()

        findItem = "SELECT * FROM brick_sets WHERE name = ?"
        cursor.execute(findItem, [item])
        results2 = cursor.fetchall()

        if results1:
            for row in results1:
                # print(row[0])
                item = row[0]
            found = 1
        elif results2:
            for row in results2:
                # print(row[2])
                item = row[2]
            found = 1
        else:
            print("Item was not found")

    # get price of item
    cursor.execute("SELECT price FROM bricks WHERE part_num = '%s' " % item)
    results = cursor.fetchall()
    for row in results:
        price = row[0]
        # print(price)

    cursor.execute("SELECT b.price FROM brick_sets a "
                   "INNER JOIN (SELECT brick_set_parts.set_id, SUM(bricks.price) as price FROM bricks "
                   "INNER JOIN brick_set_parts ON bricks.part_num = brick_set_parts.part_num "
                   "GROUP BY brick_set_parts.set_id) b "
                   "ON a.set_id = b.set_id WHERE a.name = '%s' " % item)
    results = cursor.fetchall()
    for row in results:
        # print(row[0])
        price = row[0]

    creditcard = 0
    cart = numpy.append(cart, [[var_UID, item, price, order_date, creditcard]], axis=0)


def viewCart():
    items = cart[:, 1]
    prices = cart[:, 2]

    print("Your Cart")
    print("%-15s %s" % ("Item", "Price"))
    print("%-15s %s" % (*items,  str(*prices)))

    # add total

# def deleteFromCart():


# def placeOrder():


def add_emp():
    while True:
        print("Who would you like to add? ")
        name = input("Name: ")
        cursor = conn.cursor()
        findName = "SELECT * FROM employees WHERE name = ?"
        cursor.execute(findName, [name])

        if cursor.fetchall():
            print("Name already exists. Please try again.")
            emp_management()

        insert_emp = '''INSERT INTO employees(name)
                        VALUES (?)'''
        cursor.execute(insert_emp, [name])
        conn.commit()


def emp_menu():
    print("---------- Employee Menu ----------")
    print("1. Sale")
    print("2. Manage")
    print("3. Profile")
    print("x. Exit")
    function = input("Function: ")
    if function == "x":
        main_menu()
    elif function == "2":
        manager_menu()


def manager_menu():
    print("---------- Management Menu ----------")
    print("1. Employee Management")
    print("2. Product Management")
    print("3. Store Management")
    print("4. Inventory Management")
    print("5. Reports")
    print("x. Exit")
    choice = input()
    if choice == "1":
        emp_management()
    elif choice == "x":
        sys.exit()


def store_management():
    print("---------- Stores ----------")


def emp_management():
    print("L. List Employees")
    print("S. Search Employees")
    print("A. Add Employees")
    print("x. Exit")

    choice = input()
    if choice == "L":
        read('employees')
    elif choice == "A":
        add_emp()
    elif choice == "x":
        manager_menu()


def main_menu():
    print("---------- Application Menu ----------")
    print("1.   Employee")
    print("2.   Customer")
    print("x.   Exit")
    choice = input("Application: ")
    print(choice)
    if choice == "1":
        emp_login()
        emp_menu()
    elif choice == "2":
        login(conn)

    elif choice == "x":
        sys.exit()


# login(conn)
# addToCart()
# viewCart()
main_menu()

conn.close()

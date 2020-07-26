# import cursor as cursor
import numpy
import pyodbc
from datetime import date

# global var_UID

cart = numpy.empty((0, 6), str)
order_date = date.today()

conn = pyodbc.connect(

    'Driver={SQL Server};'
    'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    # Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'

    'Database=LegoStore;'
    'Trusted_Connection=yes;'

)

cursor = conn.cursor()


# function to read from specified table. used for testing purposes
def read(table_name):
    # print("Read")
    cursor = conn.cursor()
    cursor.execute("Select * FROM " + table_name)
    for row in cursor:
        print(row)
        # print(f'row = {row}')
    print()


def login():
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
                    # var_UID = int(row[0])  # global var_UID
                    print(var_UID)
                    return "exit"
            else:
                print("Username and password not recognized")


def newCustomer():
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
    # print(var_UID)

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

    # get quantity
    found = 0
    while found == 0:
        quantity = int(input("How many " + item + "'s would you like to order: "))
        if quantity <= 0:
            print("Please enter an acceptable quantity")
        else:
            found = 1

    # get price of item
    cursor.execute("SELECT price, quantity FROM bricks WHERE part_num = '%s' " % item)
    results = cursor.fetchall()
    for row in results:
        if row[1] - quantity < 0:
            print("There is not enough stock for " + item + "\n")
            return
        else:
            price = row[0] * quantity

    cursor.execute("SELECT b.price, a.quantity FROM brick_sets a "
                   "INNER JOIN (SELECT brick_set_parts.set_id, SUM(bricks.price) as price FROM bricks "
                   "INNER JOIN brick_set_parts ON bricks.part_num = brick_set_parts.part_num "
                   "GROUP BY brick_set_parts.set_id) b "
                   "ON a.set_id = b.set_id WHERE a.name = '%s' " % item)
    results = cursor.fetchall()
    for row in results:
        if row[1] - quantity < 0:
            print("There is not enough stock for " + item + "\n")
            return
        else:
            price = row[0] * quantity

    credit_card = 0
    cart = numpy.append(cart, [[var_UID, quantity, item, price, order_date, credit_card]], axis=0)


def viewCart():
    print("Your Cart")
    print("%-10s %-15s %s" % ("Quantity", "Item", "Price"))
    for i in cart:
        print("%-10s %-15s %s" % (i[1], i[2], i[3]))

    # get total
    total = 0
    for i in cart:
        total += i[3]
    print("Total = $" + str(total))


def placeOrder():
    global cart
    viewCart()
    credit_card = input("\nPlease enter your credit card number: ")
    cursor = conn.cursor()
    insertData = """INSERT INTO orders (customer_id, quantity, item, price, order_date, creditcard)
                    VALUES (?,?,?,?,?,?)"""
    for i in cart:
        cursor.execute(insertData, [i[0], i[1], i[2], i[3], i[4], credit_card])
        deductInventory(i[1], i[2])
    conn.commit()

    # empty cart after placing order
    cart = numpy.delete(cart, numpy.s_[0:10], 0)


def deductInventory(quantity, item):
    cursor = conn.cursor()
    findItem = "SELECT * FROM bricks WHERE part_num = ?"
    cursor.execute(findItem, [item])
    results1 = cursor.fetchall()

    findItem = "SELECT * FROM brick_sets WHERE name = ?"
    cursor.execute(findItem, [item])
    results2 = cursor.fetchall()

    if results1:  # bricks
        cursor.execute("UPDATE bricks SET quantity -= ? WHERE part_num = ?", (quantity, item))
        conn.commit()
    elif results2:  # sets
        for row in results2:
            cursor.execute("UPDATE brick_sets SET quantity -= ? WHERE set_id = ?", (quantity, row[0]))
            conn.commit()
            cursor.execute("SELECT bsp.part_num "
                           "FROM brick_sets INNER JOIN brick_set_parts bsp ON brick_sets.set_id = bsp.set_id "
                           "WHERE bsp.set_id = ?", row[0])
            results3 = cursor.fetchall()
            for part in results3:
                cursor.execute("UPDATE bricks SET quantity -= 1 WHERE part_num = ?", part)


def history():
    cursor = conn.cursor()
    cursor.execute("Select quantity, item, price, order_date, creditcard FROM orders "
                   "Where customer_id = ? ORDER BY order_date desc ", var_UID)
    print("Previous Orders")
    print("%-10s %-15s %-10s %-20s %s" % ("Quantity", "Item", "Price", "Date Ordered", "Credit Card"))
    for row in cursor:
        print("%-10s %-15s %-10s %-20s %s" % (row[0], row[1], row[2], row[3], row[4]))
    print()


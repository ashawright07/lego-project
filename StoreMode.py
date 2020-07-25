import pyodbc
import random
import datetime
from datetime import date

#from Menu import *
list = []



conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    # 'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    'Server=DESKTOP-Q55TSGL;'
    'Database=LegoStore;'
    'Trusted_Connection=yes;'

)
cursor = conn.cursor()


def emp_login():
    global emp_id
    while True:
        username = input("username: ")
        password = input("password: ")
        cursor = conn.cursor()
        find_employee = "SELECT * FROM employee_login WHERE username = ? AND password = ?"
        find_access_level = "SELECT * FROM employees WHERE emp_name = ?"
        cursor.execute(find_employee, [username, password])
        results = cursor.fetchall()
        cursor.execute(find_access_level, [username])
        result = cursor.fetchall()
        employee = result[0]
        emp_id = employee[0]
        print(employee[0])

        if results:
            for row in results:
                print("Welcome " + row[0])
                return employee[2]
                #return "exit"
        else:
            print("Username and/or password not recognized")


def add_emp():
    while True:
        print("Who would you like to add? ")
        name = input("Name: ")
        cursor = conn.cursor()
        findName = "SELECT * FROM employees WHERE emp_name = ?"
        cursor.execute(findName, [name])

        if cursor.fetchall():
            print("Employee already exists. Please try again.")

        insert_emp = '''INSERT INTO employees(emp_name)
                        VALUES (?)'''
        insert_emp_login = '''INSERT INTO employee_login(username,password)
                                VALUES (?,'pass')'''
        cursor.execute(insert_emp, [name])
        cursor.execute(insert_emp_login, [name])
        conn.commit()
        break


def del_emp():
    while True:
        print("Who would you like to remove? ")
        name = input("Name: ")
        cursor = conn.cursor()
        findName = "SELECT * FROM employees WHERE emp_name = ?"
        cursor.execute(findName, [name])

        if (cursor.fetchall()):
            delete_emp = '''DELETE FROM employees WHERE emp_name = ? '''
            cursor.execute(delete_emp, [name])
            conn.commit()

        print("Employee doesn't exists. Please try again.")
        break

def srch_emp():
    while True:
        print("Who would you like to search? ")
        name = input("Name: ")
        cursor = conn.cursor()
        findName = "SELECT * FROM employees WHERE emp_name = ?"
        cursor.execute(findName, [name])
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Employee exists with an id " + str(row[0]))
            break
                #manager_menu()
        print("Employee doesn't exists. Please try again.")
        break

def Take_Order():
    items = int(input("Enter the number of items: "))
    while True:
        r = random.randint(1, 1000000)
        if r not in list:
            list.append(r)
            order_number = r
            break
    order_date = datetime.date.today()
    employee_id = emp_id
    payment_type = input("Enter the payment type: ")
    if payment_type.lower() != "cash":
        card_number = input("Enter the card number: ")
    else:
        card_number = ""
    total_amount = 0
    for i in range(items):

        item_id = input("Enter Item Id: ")
        item_description = input("Enter Item Description: ")
        quantity = int(input("Enter Quantity: "))
        item_type = input("Enter Item Type: ")
        if (item_type.lower() == "brick"):
            item_price = "SELECT price FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_price = "SELECT SUM(price) AS price FROM bricks INNER JOIN brick_set_parts ON bricks.part_num = brick_set_parts.part_num WHERE set_id = ?"
        cursor.execute(item_price, [item_id])
        res = cursor.fetchall()
        a = res[0]
        price = quantity * float(a[0])
        insert_order = ('INSERT INTO Store_Orders(order_id, order_date, emp_id, item_type, item_id, item_description, quantity, price,total_amount, payment_type, card_number) \n'
                  '                        VALUES (?,?,?,?,?,?,?,?,?,?,?)')
        cursor.execute(insert_order, [order_number, order_date, employee_id, item_type, item_id, item_description, quantity, price, total_amount, payment_type, card_number])


        total_amount = total_amount + price

    update_order = "UPDATE Store_Orders SET total_amount = ? WHERE order_id = ?"
    cursor.execute(update_order,[total_amount,order_number])
    if (item_type.lower() == "brick"):
        item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
    elif (item_type.lower() == "set"):
        item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
    cursor.execute(item_quantity, [item_id])
    a = cursor.fetchall()
    prev_quantity = a[0]
    inc_quantity = int(prev_quantity[0]) - quantity
    if (item_type.lower() == "brick"):
        updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
    elif (item_type.lower() == "set"):
        updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
    cursor.execute(updated_quantity, [inc_quantity, item_id])
    conn.commit()
    print("Order Successful.")

def Return_Order():
    items = int(input("Enter the number of items: "))
    order_number = int(input("Enter the order number: "))
    return_date = datetime.date.today()
    employee_id = emp_id
    payment_type = input("Enter the payment type: ")
    if payment_type.lower() != "cash":
        card_number = input("Enter the card number: ")
    else:
        card_number = ""
    for i in range(items):

        item_id = input("Enter Item Id: ")
        quantity = int(input("Enter Quantity: "))
        item_type = input("Enter Item Type: ")
        if (item_type.lower() == "brick"):
            item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
        cursor.execute(item_quantity, [item_id])
        a = cursor.fetchall()
        prev_quantity = a[0]
        inc_quantity = quantity + int(prev_quantity[0])
        if (item_type.lower() == "brick"):
            updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
        cursor.execute(updated_quantity, [inc_quantity, item_id])
        cnt = "SELECT COUNT(*) FROM Store_Orders WHERE order_id = ?"
        cursor.execute(cnt, [order_number])
        c = cursor.fetchall()
        d = c[0]
        count = int(d[0])
        if count > 1:
            item_price = "SELECT price,total_amount FROM Store_Orders WHERE order_id = ? AND item_id = ?"
            cursor.execute(item_price, [order_number,item_id])
            res = cursor.fetchall()
            print(res)
            a = res[0]
            b = a[0]
            y = a[1]
            return_amount = b
            updt_amount = y - b

        insert_order = (
            'INSERT INTO Return_Store_Orders(order_id, return_date, emp_id, item_type, item_id, quantity, return_amount, payment_type, card_number) \n'
            '                        VALUES (?,?,?,?,?,?,?,?,?)')
        cursor.execute(insert_order,
                       [order_number, return_date, employee_id, item_type, item_id, quantity, return_amount, payment_type, card_number])

    update_order = "DELETE FROM Store_Orders WHERE order_id = ? AND item_id = ?; UPDATE  Store_Orders SET total_amount = ? WHERE order_id = ?"

    cursor.execute(update_order, [order_number, item_id, updt_amount, order_number])
    conn.commit()
    print("Order returned Successfully.")
















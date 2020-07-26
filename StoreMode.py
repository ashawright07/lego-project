import calendar

import pyodbc
import random
import datetime
from datetime import datetime, timedelta
from calendar import monthrange

#from Menu import *
list = []
list1 = []
lst = []


conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    # 'Server=DESKTOP-Q55TSGL;'
    # 'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
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
                # return "exit"
        else:
            print("Username and/or password not recognized")

def list_emp():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    print("%-10s %-15s %-10s %s" % ("Employee_Id", "Employee_Name", "Access_Level","Store_Id"))
    for row in cursor:
        print("%-10s %-16s %-13s %s" % (row[0], row[1], row[2],row[3]))


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

        print("Employee has been removed.")
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
    order_date = datetime.now().date()
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
        if (item_type.lower() == "brick"):
            item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
        cursor.execute(item_quantity, [item_id])
        a = cursor.fetchall()
        prev_quantity = a[0]
        inc_quantity = abs(int(prev_quantity[0]) - quantity)
        if (item_type.lower() == "brick"):
            updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
        cursor.execute(updated_quantity, [inc_quantity, item_id])

    update_order = "UPDATE Store_Orders SET total_amount = ? WHERE order_id = ?"
    cursor.execute(update_order,[total_amount,order_number])

    conn.commit()
    print("Order Successful.")

def Return_Order():
    items = int(input("Enter the number of items: "))
    order_number = int(input("Enter the order number: "))
    return_date = datetime.now().date()
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

def bricks_inv():
    cursor = conn.cursor()
    cursor.execute("SELECT part_num,description,quantity FROM bricks")
    print("%-10s %-15s %s" % ("Part Number", "Part Description", "Quantity"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))

def sets_inv():
    cursor = conn.cursor()
    cursor.execute("SELECT set_id,name,quantity FROM brick_sets")
    print("%-10s %-15s %s" % ("Set Id", "Set Description", "Quantity"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))

def order_inv():
    items = int(input("Enter the number of items: "))
    while True:
        r = random.randint(1, 1000000)
        if r not in list1:
            list1.append(r)
            order_number = r
            break
    order_date = datetime.now().date()
    employee_id = emp_id
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
        insert_order = (
            'INSERT INTO Inventory_Orders(order_id, order_date, emp_id, item_type, item_id, item_description, quantity, item_price,total_amount) \n'
            '                        VALUES (?,?,?,?,?,?,?,?,?)')
        cursor.execute(insert_order,
                       [order_number, order_date, employee_id, item_type, item_id, item_description, quantity, price,total_amount])

        total_amount = total_amount + price
        if (item_type.lower() == "brick"):
            item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
        cursor.execute(item_quantity, [item_id])
        a = cursor.fetchall()
        prev_quantity = a[0]
        inc_quantity = int(prev_quantity[0]) + quantity
        if (item_type.lower() == "brick"):
            updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
        cursor.execute(updated_quantity, [inc_quantity, item_id])

    update_order = "UPDATE Inventory_Orders SET total_amount = ? WHERE order_id = ?"
    cursor.execute(update_order, [total_amount, order_number])

    conn.commit()
    print("Inventory ordered successfully.")

def reorder_inv():
    prev_order_number = int(input("Enter the order number to reorder: "))
    while True:
        r = random.randint(1, 1000000)
        if r not in lst:
            lst.append(r)
            order_number = r
            break
    order_date = datetime.now().date()
    employee_id = emp_id
    #cursor = conn.cursor()
    #item_id = "SELECT item_id FROM Inventory_Orders WHERE order_id = ?"
    cursor.execute("SELECT item_id FROM Inventory_Orders WHERE order_id = ?", [prev_order_number])
    for row in cursor.fetchall():
        item_id = row[0]
        details = "SELECT item_type,item_id,item_description,quantity,item_price,total_amount FROM Inventory_Orders WHERE order_id = ? AND item_id = ?"
        cursor.execute(details,prev_order_number,item_id)
        order = cursor.fetchall()
        order_details = order[0]
        item_type = order_details[0]
        item_id = order_details[1]
        item_description = order_details[2]
        quantity = order_details[3]
        item_price = order_details[4]
        total_amount = order_details[5]


        cursor.execute("INSERT INTO Inventory_Orders (order_id, order_date, emp_id, item_type, item_id, item_description, quantity, item_price,total_amount) VALUES (?,?,?,?,?,?,?,?,?)",order_number,order_date,employee_id,item_type, item_id, item_description, quantity, item_price,total_amount)
        if (item_type.lower() == "brick"):
            item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
        cursor.execute(item_quantity, [item_id])
        a = cursor.fetchall()
        prev_quantity = a[0]
        inc_quantity = int(prev_quantity[0]) + quantity
        if (item_type.lower() == "brick"):
            updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
        cursor.execute(updated_quantity, [inc_quantity, item_id])
    conn.commit()
    print("Reordered Successfully.")



def cancel_order():
    order_number = int(input("Enter the order number to cancel: "))
    cursor = conn.cursor()
    cursor.execute("SELECT order_id,order_date,emp_id,item_type,item_id,item_description,quantity,item_price,total_amount FROM Inventory_Orders WHERE order_id = ?",order_number)
    #res = cursor.fetchall()
    for rw in cursor.fetchall():
        insert_cancel_order = "INSERT INTO Cancelled_Inventory_Orders (order_id,order_date,emp_id,item_type,item_id,item_description,quantity,item_price,total_amount) VALUES(?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_cancel_order, [rw[0],rw[1],rw[2],rw[3],rw[4],rw[5],rw[6],rw[7],rw[8]])
        item_type = rw[3]
        quantity = rw[6]
        item_id = rw[4]
        if (item_type.lower() == "brick"):
            item_quantity = "SELECT quantity FROM bricks WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            item_quantity = "SELECT quantity  FROM brick_sets WHERE set_id = ?"
        cursor.execute(item_quantity, [item_id])
        a = cursor.fetchall()
        prev_quantity = a[0]
        inc_quantity = abs(quantity - int(prev_quantity[0]))
        if (item_type.lower() == "brick"):
            updated_quantity = "UPDATE  bricks SET quantity = ? WHERE part_num = ?"
        elif (item_type.lower() == "set"):
            updated_quantity = "UPDATE  brick_sets SET quantity = ? WHERE set_id = ?"
        cursor.execute(updated_quantity, [inc_quantity, item_id])

    cancel_order = "DELETE FROM Inventory_Orders WHERE order_id = ?"
    cursor.execute(cancel_order,[order_number])
    conn.commit()
    print("Order Cancelled Successfully.")

def daily_report():
    dt = datetime.now().date()
    cursor.execute("SELECT FORMAT(order_date,'MM-dd-yyyy'),COUNT(*),SUM(price) FROM Store_Orders WHERE order_date = ? GROUP BY order_date",dt)
    print("Daily Sales Report")
    print("%-10s %-15s %s" % ("Date", "Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))
    print("Daily Employee Status")
    cursor.execute("SELECT FORMAT(order_date,'MM-dd-yyyy'),employee_log.emp_id, emp_name,hours_worked,COUNT(*),SUM(price) FROM Store_Orders INNER JOIN employee_log ON Store_Orders.emp_id = employee_log.emp_id AND Store_Orders.order_date = employee_log.worked_date  WHERE order_date = ? GROUP BY order_date,employee_log.emp_id,emp_name,hours_worked",dt)
    print("%-10s %-15s %-15s %-10s %-10s %s" % ("Date", "Employee_Id","Employee_Name","Hours_Worked","Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %-15s %-12s %-12s %s" % (row[0], row[1], row[2],row[3],row[4],row[5]))

def weekly_report():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    cursor.execute("SELECT FORMAT(order_date,'MM-dd-yyyy'),COUNT(*),SUM(DISTINCT(total_amount)) FROM Store_Orders WHERE order_date between ? AND ? GROUP BY order_date",str(start),str(end))
    print("Weekly Sales Report")
    print("%-10s %-15s %s" % ("Date", "Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))
    print("Weekly Employee Status")
    cursor.execute("SELECT FORMAT(order_date,'MM-dd-yyyy') AS [Date] ,employee_log.emp_id, emp_name,hours_worked,COUNT(*),SUM(price) "
                   "FROM Store_Orders INNER JOIN employee_log ON Store_Orders.emp_id = employee_log.emp_id AND Store_Orders.order_date = employee_log.worked_date "
                   "WHERE order_date between ? AND ? GROUP BY order_date,employee_log.emp_id,emp_name,hours_worked",str(start),str(end))
    print("%-10s %-15s %-15s %-10s %-10s %s" % ("Date", "Employee_Id","Employee_Name","Hours_Worked","Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %-15s %-12s %-12s %s" % (row[0], row[1], row[2],row[3],row[4],row[5]))


def monthly_report():
    num_days = calendar.monthrange(datetime.now().year, datetime.now().month)
    given_date = datetime.today().date()
    first_day = given_date.replace(day=1)
    last_day = given_date.replace(day=monthrange(given_date.year, given_date.month)[1])
    cursor.execute("SELECT FORMAT(order_date,'MM-dd-yyyy'),COUNT(*),SUM(DISTINCT(total_amount)) FROM Store_Orders WHERE order_date between ? AND ? GROUP BY order_date",str(first_day),str(last_day))
    print("Monthly Sales Report")
    print("%-10s %-15s %s" % ("Date", "Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %s" % (row[0], row[1], row[2]))
    print("Monthly Employee Status")
    cursor.execute(
        "SELECT FORMAT(order_date,'MM-dd-yyyy') AS [Date] ,employee_log.emp_id, emp_name,hours_worked,COUNT(*),SUM(price) "
        "FROM Store_Orders INNER JOIN employee_log ON Store_Orders.emp_id = employee_log.emp_id AND Store_Orders.order_date = employee_log.worked_date "
        "WHERE order_date between ? AND ? GROUP BY order_date,employee_log.emp_id,emp_name,hours_worked", str(first_day),
        str(last_day))
    print("%-10s %-15s %-15s %-10s %-10s %s" % ("Date", "Employee_Id", "Employee_Name", "Hours_Worked", "Total_Orders", "Total_Revenue"))
    for row in cursor:
        print("%-10s %-15s %-15s %-12s %-12s %s" % (row[0], row[1], row[2], row[3], row[4], row[5]))

def delivery_mngt():
    cursor.execute("SELECT order_id,order_date FROM Orders")
    print("%-10s %-15s %s" % ("Order_Id", "Order_Date", "Delivery_Date"))
    for row in cursor.fetchall():
        ordr_id = row[0]
        dt = row[1]
        dlvry_dt = dt + timedelta(days=7)
        print("%-10s %-15s %s" % (row[0], row[1], dlvry_dt))


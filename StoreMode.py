import pyodbc
import sys

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    # 'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
    'Database=LegoStore;'
    'Trusted_Connection=yes;'

)

cursor = conn.cursor()


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


def add_emp():
    emp_exists = 0

    while emp_exists == 0:
        name = input("Which employee would you like to add?: ")
        empID = input("Please enter their employee ID: ")
        cursor = conn.cursor()
        findEmp = "SELECT * FROM employees WHERE name = ? AND employeeID = ?"
        cursor.execute(findEmp, [name, empID])

        if cursor.fetchall():
            print("Employee does not exist. Please try again.")
        else:
            emp_exists = 1
            insertEmp = '''INSERT INTO employees(name,employeeID) 
                    VALUES (?,?)'''
            cursor.execute(insertEmp, [name, empID])

            conn.commit()
            break


def remove_emp():
    while True:
        print("Who would you like to remove? ")
        name = input("Name: ")
        empID = input("ID: ")
        cursor = conn.cursor()
        deleteName = "SELECT * FROM employees WHERE name = ? AND employeeID = ?"
        cursor.execute(deleteName, [name, empID])

        delete_emp = ''' DELETE FROM employees WHERE name = ? AND employeeID = ?'''
        cursor.execute(delete_emp, [name, empID])
        conn.commit()
        print(name + " has been removed.")
        break


def search_emp():
    while True:

        name = input("Who are you looking for?: ")
        empID = input("ID: ")
        cursor = conn.cursor()
        emp_search = "SELECT * FROM employees WHERE name = ? AND employeeID = ?"
        cursor.execute(emp_search, [name, empID])

        results = cursor.fetchone()

        if results:
            print(results)
        else:
            print(name + " ", empID, " could not be found")

        conn.commit()
        break

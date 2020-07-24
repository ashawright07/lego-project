import pyodbc


conn = pyodbc.connect(
    'Driver={SQL Server};'
    # 'Server=NOTAMAC\\MYSERVER;'  # i am using a different server when testing db, but it works
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
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
    while True:
        print("Who would you like to add? ")
        name = input("Name: ")
        cursor = conn.cursor()
        findName = "SELECT * FROM employees WHERE name = ?"
        cursor.execute(findName, [name])

        if cursor.fetchall():
            print("Name already exists. Please try again.")

        insert_emp = '''INSERT INTO employees(name)
                        VALUES (?)'''
        cursor.execute(insert_emp, [name])
        conn.commit()

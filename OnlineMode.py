import pyodbc


# function to read from specified table
def read(table_name):
    # print("Read")
    cursor = conn.cursor()
    cursor.execute("Select * FROM " + table_name)
    for row in cursor:
        print(f'row = {row}')
    print()


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
                    print("Welcome " + row[1])
                    # global var_UID
                    var_UID = int(row[0])
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
    insertData = '''INSERT INTO customerInfo(customer_id, f_name, l_name, email, phone, address, username, password) 
                        VALUES (?,?,?,?,?,?,?,?)'''
    cursor.execute(insertData, [var_UID, f_name, l_name, email, phone, address, username, password])

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
    'Database=LegoStore;'
    'Trusted_Connection=yes;'
)

global var_UID

# newCustomer(conn)
read('login')
# login(conn)

conn.close()

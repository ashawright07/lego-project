import pyodbc


def read(conn):
    # print("Read")
    cursor = conn.cursor()
    cursor.execute("Select * FROM login")
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
            find_user = "SELECT * FROM login WHERE username = ? AND password = ? AND user_type = 'customer'"
            cursor.execute(find_user, [username, password])
            results = cursor.fetchall()

            if results:
                for row in results:
                    print("Welcome " + row[1])
                    global var_UID
                    var_UID = int(row[0])
                    # print(var_UID)
                    return "exit"
            else:
                print("Username and password not recognized")


def newCustomer(conn):
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
    user_type = 'customer'
    while password != password1:
        print("Your passwords don't match. Please try again.")
        password = input("Please enter your password: ")
        password1 = input("Please reenter your password: ")
    insertData = '''INSERT INTO login(username,password,user_type) 
                    VALUES (?,?,?)'''
    cursor.execute(insertData, [username, password, user_type])
    conn.commit()


conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
    'Database=LegoStore;'
    'Trusted_Connection=yes;'
)

# newCustomer(conn)
read(conn)
login(conn)

conn.close()

import pyodbc

def read(conn):
    #print("Read")
    cursor = conn.cursor()
    cursor.execute("Select * FROM login")
    for row in cursor:
        print(f'row = {row}')
    print()


def login(conn):
    while True:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        cursor = conn.cursor()
        find_user = ("SELECT * FROM login WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()

        if results:
            for row in results:
                print("Welcome " + row[1])
                global var_UID
                var_UID = int(row[0])
              #  print(var_UID)
                return ("exit")
        else:
            print("Username and password not recognized")


conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-UMJ1B2A\MSSQLSERVER2020;'
    'Database=LegoStore;'
    'Trusted_Connection=yes;'
)

read(conn)
login(conn)

conn.close()
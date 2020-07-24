from OnlineMode import *
from StoreMode import *
import sys


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
        login()

    elif choice == "x":
        sys.exit()


main_menu()

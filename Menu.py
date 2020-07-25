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


def customer_menu():
    print("---------- Customer Menu ----------")
    print("1. Browse Items")
    print("2. Search Items")
    print("3. Customer Information")
    print("Payment Information")

    choice = input("What would like to do?: ")

    if choice == "1":
        browse()
    elif choice == "2":
        search()
    # elif choice == "3":


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
        emp_menu()
        # sys.exit()


def emp_management():
    # while True:
    print("L. List Employees")
    print("S. Search Employees")
    print("A. Add Employees")
    print("R. Remove Employee")
    print("x. Exit")

    choice = input()
    if choice == "l":
        read('employees')

    elif choice == "a":
        add_emp()

    elif choice == "r":
        remove_emp()

    elif choice == "x":
        manager_menu()


def main_menu():
    while True:
        print("---------- Application Menu ----------")
        print("1.   Employee")
        print("2.   Customer")
        print("x.   Exit")
        choice = input("Application: ")
        if choice == "1":
            emp_login()
            emp_menu()

        elif choice == "2":
            login()
            customer_menu()

        elif choice == "x":
            print("Goodbye!")
            sys.exit()


main_menu()

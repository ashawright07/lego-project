from OnlineMode import *
from StoreMode import *
import sys

def sale_menu():
    print("---------- Sale Menu ----------")
    print("1. Take Order")
    print("2. Return Order")
    print("x. Exit")
    function = input("Function: ")
    if function == "1":
        Take_Order()
        if var == 0:
            emp_menu_0()
        elif var == 1:
            emp_menu_1()
        else:
            emp_menu_0()
    elif function == "2":
        Return_Order()
        if var == 0:
            emp_menu_0()
        elif var == 1:
            emp_menu_1()
        else:
            emp_menu_0()
    elif function == "x":
        if var == 0:
            emp_menu_0()
        elif var == 1:
            emp_menu_1()
        else:
            emp_menu_0()


def emp_menu_1():
    print("---------- Employee Menu ----------")
    print("1. Sale")
    print("2. Manage")
    print("x. Exit")
    function = input("Function: ")
    if function == "1":
        sale_menu()
    elif function == "2":
        manager_menu()
    elif function == "x":
        main_menu()

def emp_menu_0():
    print("---------- Employee Menu ----------")
    print("1. Sale")
    print("x. Exit")
    function = input("Function: ")
    if function == "1":
        sale_menu()
    elif function == "x":
        main_menu()

def inv_management():
    print("---------- Inventory Menu ----------")
    print("1. Bricks Inventory")
    print("2. Sets Inventory")
    print("3. Order Inventory")
    print("4. Reorder Inventory")
    print("5. Cancel Order")
    print("x. Exit")
    choice = input("Choice: ")
    if choice == "1":
        bricks_inv()
    elif choice == "2":
        sets_inv()
    elif choice == "3":
        order_inv()
    elif choice == "4":
        reorder_inv()
    elif choice == "5":
        cancel_order()
    elif choice == "x":
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
        addToCart()
        viewCart()
        placeOrder()
    elif choice == "2":
        search()
        addToCart()
        viewCart()
        placeOrder()
    # elif choice == "3":
        # show_customer_info()
        # viewCart()


def manager_menu():
    print("---------- Management Menu ----------")
    print("1. Employee Management")
    print("2. Product Management")
    print("3. Store Management")
    print("4. Inventory Management")
    print("5. Reports")
    print("x. Exit")
    choice = input("Choice: ")
    if choice == "1":
        emp_management()
    elif choice == "4":
        inv_management()
    elif choice == "5":
        reports()
    elif choice == "x":
        main_menu()

def reports():
    print("---------- Reports Menu ----------")
    print("1. Daily Report")
    print("2. Weekly Report")
    print("3. Monthly Report")
    print("x. Exit")
    choice = input("Choice: ")
    if choice == "1":
        daily_report()
    elif choice == "2":
        weekly_report()
    elif choice == "3":
        monthly_report()
    elif choice == "x":
        manager_menu()

def emp_management():
    print("L. List Employees")
    print("S. Search Employees")
    print("A. Add Employees")
    print("D. Remove Employees")
    print("x. Exit")

    choice = input("Choice: ")
    if choice == "L":
        read('employees')
        emp_management()
    elif choice == "S":
        srch_emp()
        emp_management()
    elif choice == "A":
        add_emp()
        emp_management()
    elif choice == "D":
        del_emp()
        emp_management()
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
        global var
        var = emp_login()
        if var == 0:
            emp_menu_0()
        elif var == 1:
            emp_menu_1()
        else:
            emp_menu_0()
    elif choice == "2":
        login()
        customer_menu()
    elif choice == "x":
        print("Goodbye!")
        sys.exit()


main_menu()

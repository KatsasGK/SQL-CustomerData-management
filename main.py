import mysql
from mysql.connector import Error
from connection_test import connection_test
from tabulate import tabulate
import smtplib
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from datetime import datetime
from datetime import date
from colorama import Fore,Style
from colorama import init
init()


pins = 3
# FIRST AUTHENTICATION
with open("credentials.txt") as file:
    # GET PASSWD HERE AND OTHER CREDENTIALS
    credentials = file.readlines()
    masterpass = credentials[0].strip()
    host = credentials[1].strip()
    database = credentials[2].strip()
    user = credentials[3].strip()
    password = credentials[4].strip()
    gmail_user = credentials[5].strip()
    gmail_password = credentials[6].strip()
    gmail_recipient = credentials[7].strip()

def loggin(user_name_trap):
    logging.basicConfig(filename="logs.txt",filemode="a", format='%(asctime)s - %(message)s', level=logging.INFO)
    #logging.info('{} logged in'.format(user_name_trap))

    file = open("logs.txt", "a")
    info = logging.info('{} logged in'.format(user_name_trap))
    file.write("\n")


def logout(user_name_trap):
    logging.basicConfig(filemode="logs.txt", format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    #logging.warning('{} logged out'.format(user_name_trap))

    file = open("logs.txt", "a")
    info = logging.info('{} logged out'.format(user_name_trap))
    file.write("\n")


# FOR CORRECT LOGIN
def send_email_alert_LOGIN(gmail_user,gmail_password,gmail_recipient,user_name_trap):
    msg = MIMEMultipart()
    msg['Subject'] = "ALERT FOR 'CORRECT' LOGIN"
    msg['From'] = gmail_user
    msg['To'] = gmail_recipient
    msg.preamble = 'preamble'

    body = ("Someone is using NOW the MYSQL-DATABASE-MANAGER (He guessed CORRECTLY)\n"
            "And he claims to be {}".format(user_name_trap))


    msg = MIMEText(body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, gmail_recipient, msg.as_string())
    server.quit()

    loggin(user_name_trap)


# UNABLE TO LOGIN
def send_email_alert_wrong_login(gmail_user,gmail_password,gmail_recipient,user_name_trap):
    msg = MIMEMultipart()
    msg['Subject'] = "ALERT FOR FAILED LOGIN"
    msg['From'] = gmail_user
    msg['To'] = gmail_recipient
    msg.preamble = 'preamble'

    body = ("Someone is using NOW the MYSQL-DATABASE-MANAGER (He guessed WRONG)\n"
            "And he claims to be {}".format(user_name_trap))


    msg = MIMEText(body)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, gmail_recipient, msg.as_string())
    server.quit()

    loggin(user_name_trap)

    # VERIFY PASSWD HERE
def authenticated(pins):
    user_name_trap = input("What's your name? ")
    print("Hello ", user_name_trap)
    authentication_question = input("ENTER MASTER PASSWORD: ")

    if masterpass == authentication_question:

        # SEND ALERT FOR CORRECT LOGIN + USER
        print("Are you sure now that you are", user_name_trap, "?")
        to_avoid_confusion = input("ENTER [Yes/No] ")

        if to_avoid_confusion == "yes" or "Y" or "Yes" or "YES":
             send_email_alert_LOGIN(gmail_user, gmail_password, gmail_recipient, user_name_trap)

        elif to_avoid_confusion == "N" or "NO" or "n" or "no":
            user_name_trap = input("What was your name then? ")
            send_email_alert_LOGIN(gmail_user, gmail_password, gmail_recipient, user_name_trap)


        def customers_table():

            def show_customers():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                SELECT * FROM customers ORDER BY full_name ASC;
                """)
                outputs = cursor.fetchall()

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5], output[6] ]]
                    print(tabulate(table, headers=["Customer ID", "Full name", "Email", "Quality", "Priority", "Last Order", "Debt"]))
                    print("\n")

                prompt_order_by_quality_or_priority = input("Do you want to organise Customers by Quality or Priority?[1/2/3=NO]: ")
                if prompt_order_by_quality_or_priority == "1":
                    cursor.execute("SELECT * FROM customers ORDER BY quality ASC;")
                    outputs = cursor.fetchall()

                    for output in outputs:
                        table = [[output[0], output[1], output[2], output[3], output[4], output[5], output[6]]]
                        print(tabulate(table, headers=["Customer ID", "Full name", "Email", "Quality", "Priority",
                                                       "Last Order", "Debt"]))
                        print("\n")

                if prompt_order_by_quality_or_priority == "2":
                    cursor.execute("SELECT * FROM customers ORDER BY priority DESC;")
                    outputs = cursor.fetchall()

                    for output in outputs:
                        table = [[output[0], output[1], output[2], output[3], output[4], output[5], output[6]]]
                        print(tabulate(table, headers=["Customer ID", "Full name", "Email", "Quality", "Priority",
                                                       "Last Order", "Debt"]))
                        print("\n")


                if prompt_order_by_quality_or_priority == "3":
                    main_menu()

            def add_customers():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )

                print("Enter customer's Data\n")
                #customer_id = input("Customer's ID: ")
                full_name = input("Full name: ")
                email = input("Email: ")
                quality = input("Quality: ")
                priority = input("Priority: ")
                last_order = input("Last Order: ")
                debt = input("debt: ")

                cursor = connection.cursor()

                sql = "INSERT INTO customers (full_name,email,quality,priority,last_order,debt) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (full_name,email,quality,priority,last_order,debt)
                cursor.execute(sql,values)
                connection.commit()

                prompt_continue = input("Add more Customers? ")
                if prompt_continue == "yes":
                    add_customers()
                else:
                    main_menu()

            def remove_customers():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                               SELECT * FROM customers ORDER BY full_name ASC;
                               """)
                outputs = cursor.fetchall()

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5], output[6]]]
                    print(tabulate(table,
                                   headers=["Customer ID", "Full name", "Email", "Quality", "Priority", "Last Order",
                                            "Debt"]))
                    print("\n")

                delete = input("ENTER ID: ")
                delete_query = "DELETE FROM customers WHERE customer_id = %s"
                cursor.execute(delete_query, (delete,))
                connection.commit()

                more_delete = input("DELETED...\n"
                                    "Do you want to delete more? ")

                if more_delete == "yes":
                    remove_customers()
                else:
                    return



            # CUSTOMER MENU
            answer = input("-------AVAILABLE OPTIONS-------\n"
                           "1:Show Customers\n"
                           "2:Add Customers\n"
                           "3:Remove Customers\n"
                           "4:BACK\n"
                           "ENTER: ")
            if answer == "1":
                show_customers()
            if answer == "2":
                add_customers()
            if answer == "3":
                remove_customers()
            if answer == "4":
                main_menu()


        def goods_table():
            # OPTION 1 ADD PRODUCTS
            def name_checker(product_name):
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                global check
                check = 4

                cursor = connection.cursor()
                cursor.execute("SELECT * FROM goods WHERE name = %s", (product_name,))
                outputs = cursor.fetchall()

                if not outputs:
                    print(Fore.LIGHTGREEN_EX + "[OK]\n"
                                               "Available Name...Check",
                          Style.RESET_ALL + "")
                else:
                    print(Fore.LIGHTRED_EX + "[WARNING]\n"
                                             "Name Already Exists...",
                          Fore.RESET + "")
                    check = 1
                    return check

            def add_products(name_checker):
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                print("Enter NEW Product's Data\n")
                product_name = input("Product's Name: ")
                name_checker(product_name)
                if check == 1:
                    product_name = input("Product's Name: ")
                    price = input("price: ")
                    quality = input("Quality: ")
                    quantity = input("Quantity: ")
                    warehouse = input("Warehouse: ")

                    cursor = connection.cursor()

                    sql = "INSERT INTO goods (name,price,quality,quantity,warehouse) VALUES (%s, %s, %s, %s, %s)"
                    values = (product_name, price, quality, quantity, warehouse)
                    cursor.execute(sql, values)
                    connection.commit()
                else:

                    price = input("price: ")
                    quality = input("Quality: ")
                    quantity = input("Quantity: ")
                    warehouse = input("Warehouse: ")

                    cursor = connection.cursor()

                    sql = "INSERT INTO goods (name,price,quality,quantity,warehouse) VALUES (%s, %s, %s, %s, %s)"
                    values = (product_name, price, quality, quantity, warehouse)
                    cursor.execute(sql, values)
                    connection.commit()

                prompt_continue = input("Add more Products? ")
                if prompt_continue == "yes":
                    add_products(name_checker)
                else:
                    print("\n\n")
                goods_menu()

            # OPTION 2 REMOVE PRODUCTS
            def remove_products():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                               SELECT * FROM goods ORDER BY name ASC;
                               """)
                outputs = cursor.fetchall()

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                delete = input("ENTER ID: ")
                delete_query = "DELETE FROM goods WHERE good_id = %s"
                cursor.execute(delete_query, (delete,))
                connection.commit()

                nonstop = False
                more_delete = input("DELETED...\n"
                                    "Do you want to delete more? ")
                if more_delete == "yes":
                    remove_products()
                else:
                    goods_menu()

            # OPTION 3 SHOW AVAILABLE PRODUCTS
            def show_available_products():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT * FROM goods ORDER BY quantity DESC;
                                """)
                outputs = cursor.fetchall()

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                goods_menu()

            # OPTION 4 SEARCH FOR SPECIFIC PRODUCT IF ON STOCK
            def search_for_available_products():

                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()

                search_name = input("Which Product are you looking for?\n"
                                    "Enter: ")
                cursor.execute("SELECT * FROM goods WHERE name = %s", (search_name,))
                outputs = cursor.fetchall()

                if not outputs:
                    print(Fore.RED + "\n[WARNING]\n"
                                     "Nothing found! Please be more specific.\n",
                          Style.RESET_ALL + "")

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                goods_menu()

            # OPTION 5 PQC
            def PQC():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )

                cursor = connection.cursor()

                # HIGH Q
                cursor.execute("SELECT * FROM goods WHERE quality >= 7")
                outputs = cursor.fetchall()

                print("--------------------------------",
                      Fore.BLUE + "TOTAL HIGH QUALITY PRODUCTS LIST",
                      Style.RESET_ALL + "--------------------------------")

                if not outputs:
                    print(Fore.RED + "\n[WARNING]\n"
                                     "No High Quality Products found.\n",
                          Style.RESET_ALL + "")

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                # MEDIUM Q
                cursor.execute("SELECT * FROM goods WHERE quality < 7 AND quality >= 4")
                outputs = cursor.fetchall()

                print("--------------------------------",
                      Fore.BLUE + "TOTAL MEDIUM QUALITY PRODUCTS LIST",
                      Style.RESET_ALL + "--------------------------------")

                if not outputs:
                    print(Fore.RED + "\n[WARNING]\n"
                                     "No Medium Quality Products found.\n",
                          Style.RESET_ALL + "")

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                # LOW Q
                cursor.execute("SELECT * FROM goods WHERE quality < 4")
                outputs = cursor.fetchall()

                print("--------------------------------",
                      Fore.BLUE + "TOTAL LOW QUALITY PRODUCTS LIST",
                      Style.RESET_ALL + "--------------------------------")

                if not outputs:
                    print(Fore.RED + "\n[WARNING]\n"
                                     "No Low Quality Products found.\n",
                          Style.RESET_ALL + "")

                for output in outputs:
                    table = [[output[0], output[1], output[2], output[3], output[4], output[5]]]
                    print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality", "Quantity",
                                                   "Warehouse"]))
                    print("\n")

                goods_menu()

            # OPTION 6 LOW QUANTITY WARNINGS
            def low_quantity_warnings():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )

                cursor = connection.cursor()

                cursor.execute("SELECT * FROM goods WHERE quantity <= 100 ORDER BY quantity DESC")
                outputs = cursor.fetchall()

                if not outputs:
                    print(Fore.LIGHTGREEN_EX + "\n[ALL GOOD]\n"
                                               "Everything is in stock.\n",
                          Style.RESET_ALL + "")

                if outputs:
                    print("--------------------------------",
                          Fore.LIGHTYELLOW_EX + "WARNING! RUNNING LOW ON THESE",
                          Style.RESET_ALL + "--------------------------------")

                    for output in outputs:
                        if output[4] > 0:
                            table = [[output[0], output[1], output[2], output[3], + output[4], output[5]]]
                            print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality",
                                                           Fore.LIGHTYELLOW_EX + "Quantity" + Fore.RESET, "Warehouse"]))
                            print("\n")
                        if output[4] == 0:
                            table = [[output[0], output[1], output[2], output[3], + output[4], output[5]]]
                            print(tabulate(table, headers=["Product ID", "Product's name", "price", "Quality",
                                                           Fore.RED + "Quantity" + Fore.RESET, "Warehouse"]))
                            print("\n")

                goods_menu()

            def summary():
                print(Fore.MAGENTA + "\nSummary is not Avalaible yet. Check in the github page for more information.\n"
                                     "Thank you.\n" + Fore.RESET)
                goods_menu()

            def goods_menu():
                # GOODS MENU
                answer = input("-------AVAILABLE OPTIONS-------\n"
                               "1:Add Products\n"
                               "2:Remove Products\n"
                               "3:Show Available Products\n"
                               "4:Search for specific Product\n"
                               "5:Product Quality Check\n"
                               "6:Low Quantity Warnings\n"
                               "7:Summary\n"
                               "8:Back\n"
                               "ENTER: ")
                if answer == "1":
                    add_products(name_checker)
                if answer == "2":
                    remove_products()
                if answer == "3":
                    show_available_products()
                if answer == "4":
                    search_for_available_products()
                if answer == "5":
                    PQC()
                if answer == "6":
                    low_quantity_warnings()
                if answer == "7":
                    summary()
                if answer == "8":
                    # main_menu()
                    return

            goods_menu()
            main_menu()
            # goods_table()


        def earnings_table():
            return

        def orders_table():
            return

        def notepad():

            # FUNCTIONS HERE
            # CREATE NOTES FUNCTION
            checknote = 1
            def create_note(checknote):
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                if checknote == 1:
                    print("\nEnter NEW Note's Data")
                    topic = input("Topic: ")
                    note = input("Note: ")
                    now = datetime.now()
                    date = now.strftime("%d/%m/%Y %H:%M:%S")
                    cursor = connection.cursor()

                    sql = "INSERT INTO notepad (date_added,topic,note) VALUES (%s, %s, %s)"
                    values = (date, topic, note)
                    cursor.execute(sql, values)
                    connection.commit()
                else:
                    notepad()

                prompt_continue = input("Add more Notes? ")
                if prompt_continue == "yes":
                    create_note(checknote)
                else:
                    print("\n")
                    checknote = 2
                    notepad()

            # DELETE NOTES FUNCTION
            def delete_note():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                               SELECT * FROM notepad ORDER BY date_added DESC;
                               """)
                outputs = cursor.fetchall()
                for output in outputs:
                    print("----------------------------------------------------------------------------\n")
                    print(" ---- NOTE'S ID ----", output[0])
                    print("DATE--->", output[1])
                    print("Topic-->", output[2])
                    print(output[3])
                    print("\n")

                delete = input("ENTER ID: ")
                delete_query = "DELETE FROM notepad WHERE note_id = %s"
                cursor.execute(delete_query, (delete,))
                connection.commit()

                deletemore = input("DELETED...\n"
                                   "Do you want to delete more? ")
                if deletemore == "yes":
                    delete_note()
                else:
                    print("\n")
                    notepad()

            # SHOW NOTED FUNCTION
            def show_notes():
                connection = mysql.connector.connect(host=host,
                                                     database=database,
                                                     user=user,
                                                     password=password,
                                                     )
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT * FROM notepad ORDER BY date_added ASC;
                                """)
                outputs = cursor.fetchall()

                for output in outputs:
                    print("----------------------------------------------------------------------------\n")
                    print("DATE--->", output[1])
                    print("Topic-->", output[2])
                    print(output[3])
                    print("\n")

                """
                for output in outputs:
                    table = [output[1], output[2], output[3]]
                    print(tabulate(table, headers=["Date Added", "Topic", "Note"]))
                    print("\n")
                """

                notepad()

            # NOTEPAD MENU HERE
            def notepad_menu():
                answer = input("-------AVAILABLE OPTIONS-------\n"
                               "1:Create a Note\n"
                               "2:Delete a Note\n"
                               "3:Show Notes\n"
                               "4:Back\n"
                               "ENTER: ")
                if answer == "1":
                    create_note(checknote)
                if answer == "2":
                    delete_note()
                if answer == "3":
                    show_notes()
                if answer == "4":
                    main_menu()

            notepad_menu()

        def connection_info():
            return


        def main_menu():
            # FIRST TEST CONNECTION THEN ASK USER FOR WHAT HE NEEDS
            print("-----------------WELCOME-------------------")
            print("You are using the Database Manager. Please be carefull with your data!")

            # CHECK FOR CONNECTION HERE
            print("*This is a small check to see if the server is Up..*")

            connection_test(host,database,user,password)
            # CHECK WHAT USER NEEDS HERE

            option = input("What do you need?\n"
                           "1: CUSTOMERS\n"
                           "2: GOODS\n"
                           "3: ORDERS\n"
                           "4: Earnings\n"
                           "4: NOTEPAD\n"
                           "5: CONNECTION INFO\n"
                           "6: Logout\n"
                           "ENTER: ")
            if option == "1":
                customers_table()
            if option == "2":
                goods_table()
            if option == "3":
                print("3")
            if option == "4":
                notepad()
            if option == "5":
                print("5")
            if option == "6":
                logout(user_name_trap)

        main_menu()

    if authentication_question != masterpass:
        pins = pins - 1
        if pins > 0:
            authenticated(pins)
        if pins == 0:
            print("FAILED TO LOGIN...ALERTING ADMIN")
authenticated(pins)

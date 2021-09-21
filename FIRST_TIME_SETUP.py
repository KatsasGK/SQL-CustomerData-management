from connection_test import connection_test
#from customer_table_create import create_customer_table



from colorama import Fore,Style
from colorama import init
init()





credentials_file = open("credentials.txt","w")

master_password = input("ENTER Master Password: ")
host = input("ENTER Host: ")
database = input("ENTER Database: ")
user = input("ENTER USER: ")
password = input("ENTER PASSWORD: ")

print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("|Now you have to setup the email alert system which is 100% required for your data's latest layer of security.   |"
      "\n|First add the GMAIL USER that SENDS the data. (reccommended to create a new in case of data breach)             |")
print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

gmail_username_that_sends_email = input("SENDER'S gmail username\n"
                                        "ENTER: ")
gmail_password_that_sends_email = input("SENDER'S gmail PASSWORD\n"
                                        "ENTER: ")
gmail_account_to_send_email = input("RECIPIENT'S gmail\n"
                                    "ENTER: ")

# STORE ENCRYPTED FILES
credentials_file.write(master_password)
credentials_file.write("\n")
credentials_file.write(host)
credentials_file.write("\n")
credentials_file.write(database)
credentials_file.write("\n")
credentials_file.write(user)
credentials_file.write("\n")
credentials_file.write(password)
credentials_file.write("\n")
credentials_file.write(gmail_username_that_sends_email)
credentials_file.write("\n")
credentials_file.write(gmail_password_that_sends_email)
credentials_file.write("\n")
credentials_file.write(gmail_account_to_send_email)
credentials_file.write("\n")


# TEST CONNECTION
print("testing credentials")
connection_test(host,database,user,password)

# AFTER CONNECTION TEST CREATE ALL TABLES
print("Creating required tables...")
#create_customer_table()

credentials_file.close()

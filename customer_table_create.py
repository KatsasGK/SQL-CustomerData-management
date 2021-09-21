import mysql.connector
from mysql.connector import Error
from colorama import Fore,Style
from colorama import init
init()


with open("credentials.txt") as file:
    # GET PASSWD HERE AND OTHER CREDENTIALS
    credentials = file.readlines()
    masterpass = credentials[0].strip()
    host = credentials[1].strip()
    database = credentials[2].strip()
    user = credentials[3].strip()
    password = credentials[4].strip()

def create_customer_table():
    try:
        connection = mysql.connector.connect(host=localhost,
                                             database=database,
                                             user=user,
                                             password=password)

        # CREATE THE TABLE HERE OR CUSTOMISE IT
        cursor = connection.cursor()
        customer_table_query = """
                        CREATE TABLE CUSTOMERS (
                            customer_id INT PRIMARY KEY AUTO_INCREMENT,
                            full_name VARCHAR(40) NOT NULL,
                            email VARCHAR(25) DEFAULT 'N/A',
                            quality INT(2) DEFAULT '5',
                            priority INT(2) DEFAULT '5',
                            last_order VARCHAR(100) DEFAULT 'No last orders yet',
                            debt INT DEFAULT '0' 
                        );
                        """
        result = cursor.execute(customer_table_query)
        print("Customer Table created successfully...")

    except mysql.connector.Error as error:
        print("Error while creating the customer table", error)
    finally:
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL connection closed.")

create_customer_table()
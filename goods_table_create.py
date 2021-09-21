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

try:
    connection = mysql.connector.connect(host=host,
                                        database=database,
                                        user=user,
                                        password=password)
    cursor = connection.cursor()

    create_goods_table_query = """
        CREATE TABLE goods(
            good_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(25) NOT NULL,
            price INT NOT NULL,
            quality INT NOT NULL,
            quantity INT NOT NULL,
            warehouse VARCHAR(20) NOT NULL 
        );
    """
    cursor.execute(create_goods_table_query)
    print("Goods Table created successfully...")
except mysql.connector.Error as errors:
    print("Error while creating Goods table: " , errors)
finally:
    cursor.close()
    connection.close()

# DONT FORGET TO ADD WAREHOUSES OPTION
# IT SHOULD CONNECT WITH AVAILABLE GOODS AND ORDERS

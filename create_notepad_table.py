import mysql
from mysql.connector import Error
from connection_test import connection_test
from colorama import Fore,Style
from colorama import init
init()


# connection establish
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

    create_notepad_query = """
        CREATE TABLE NOTEPAD(
            note_id INT PRIMARY KEY AUTO_INCREMENT,
            date_added VARCHAR(22) NOT NULL,
            topic VARCHAR(35) NOT NULL,
            note VARCHAR(1000) NOT NULL
        );
    """

    cursor.execute(create_notepad_query)
    print("Successfully created notepad table...")


except mysql.connector.Error as errors:
    print("Error while creating notepad table: ", errors)
finally:
    cursor.close()
    connection.close()
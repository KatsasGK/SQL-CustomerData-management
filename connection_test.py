import mysql.connector
from mysql.connector import Error

def connection_test(host,database,user,password):
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password,
                                             use_pure=True)
        if connection.is_connected():
            server_info = connection.get_server_info()
            print("Connected to MySQL Server. Version is ", server_info)

            cursor = connection.cursor()
            cursor.execute("select database();")
            database = cursor.fetchone()
            print("Connected Database ->", database)

    except Error as e:
        print("Error while connecting to MySQL ", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

#connection_test()





"""
def send_email_alert_LOGIN(user_name_trap,gmail_user,gmail_password,gmail_recipient):
    try:
        # EMAIL
        sent_from = gmail_user
        to = gmail_recipient
        subject = "WARNING: LOGIN ALERT FOR MYSQL-DATABASE-MANAGER!"
        email_text_login = "SOMEONE is using the SQL-DATABASE-MANAGER\n" \
                           "He guessed the password correctly and he claims to be ", user_name_trap
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text_login)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')


"""

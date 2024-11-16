import mysql.connector
from mysql.connector import errorcode

def initialize_database(config):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS api_cse2")
        cursor.execute("USE api_cse2")

        # Create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
        """
        cursor.execute(create_table_query)

        print("Database and table successfully Initialized.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

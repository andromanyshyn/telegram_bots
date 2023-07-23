import psycopg2
from psycopg2 import connect
from keys.keys import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class Database():
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_connect = None

    def database_connect(self):
        try:
            self.db_connect = psycopg2.connect(
                dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            )
            self.db_connect.autocommit = True
        except psycopg2.Error as error:
            print(f"Error connecting to Database: {error}")

    def create_table(self):
        if not self.db_connect:
            raise psycopg2.OperationalError("Please connect to the Database")
        try:
            with self.db_connect.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS username(
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(64)
                    );
                    """)
        except psycopg2.Error as error:
            print(f"Error creating the table: {error}")
        print('Table Created Successfully')

    def save_in_table(self, value):
        if not self.db_connect:
            raise psycopg2.OperationalError("Please connect to the Database")
        try:
            with self.db_connect.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO username (username)
                    VALUES(
                        '{value}'
                    );
                    """
                )
        except psycopg2.Error as error:
            print(f"Error creating the table: {error}")

    def show_in_table(self):
        if not self.db_connect:
            raise psycopg2.OperationalError("Please connect to the Database")
        try:
            with self.db_connect.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT username FROM username
                    """
                )
                usernames_list = [username[0] for username in cursor.fetchall()]
        except psycopg2.Error as error:
            print(f"Error creating the table: {error}")
        return '\n'.join(usernames_list)


database = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
database.database_connect()
database.create_table()

import os
import zipfile
import psycopg2 as pg2
from psycopg2.extensions import AsIs
from os.path import join, dirname
from dotenv import load_dotenv
import json

'''
TODOS:

Write methods to get most current data to currusage table
move current currusage to prevusage
Maybe keep the table with all the data. May just go back rolling 6 months at a time for size issues and costs.
Sanitization? I don't know if its required because I control the data flow. Will sanitize during parsing, as it seems to make logical sense.
''' 
# -------------------------------
# Connection variables
# -------------------------------
# travels up a level to find the .env, then loads it below to 
# allow access to environment vars for security
dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".env")
)  
load_dotenv(dotenv_path)

# -------------------------------
# Connection to database
# -------------------------------
# Server connection
# db_url = os.environ.get("DATABASE_URL")
# CONN = pg2.connect(db_url, sslmode="require")
# print("Connected remotely.")


# -------------------------------
# Database manager class
# -------------------------------
class SQLManager:
    def __init__(self):
        self.table_name = "smogon_usage_stats"
        try:
            self.__FILE = os.path.join(os.getcwd(), "data/statsmaster.csv")
        except:
            print("you haven't downloaded any stats")

    def connect(
        self, db_name=False, user_name=False, pwd=False, hostname=False, port_num=False
    ):
        connection = pg2.connect(
            database=db_name if db_name else os.environ.get("LOCAL_DATABASE"),
            user=user_name if user_name else os.environ.get("LOCAL_USER"),
            password=pwd if pwd else os.environ.get("LOCAL_PASSWORD"),
            host=hostname if hostname else os.environ.get("LOCAL_HOST"),
            port=port_num if port_num else os.environ.get("LOCAL_PORT"),
        )

        if connection:
            self.conn = connection
            print('connected')
        else:
            print('error')
        return connection
    
    def create_cursor(self):
        '''
        If the user hasn't connected manually, no self.conn exists, so we must call it and create the cursor from default values.

        This function is here because its good practice to close the cursor after executing a command. So it is called at the top of a 
        SQL-performing function and closed after it. 
        '''
        if self.conn:
            conn = self.conn
        else:
            conn = self.connect()
            self.conn = conn
        curr = conn.cursor()
        return curr
    
    @staticmethod
    def __close_cursor(self, cursor):
        cursor.close()
    # -------------------------------
    # Create the tables for the database
    # -------------------------------
    # def construct_tables(self):
    def construct_tables(self):
        master_file = open(self.__FILE)
        columns = master_file.readline().strip().split(",")

        cursor = self.create_cursor();
        sql_cmd = "DROP TABLE IF EXISTS " + self.table_name + ";\n"
        sql_cmd += "CREATE TABLE " + self.table_name + " (\n"

        sql_cmd += (
            "id_ SERIAL PRIMARY KEY,\n"
            + columns[0]
            + " INTEGER,\n"
            + columns[1]
            + " VARCHAR(50),\n"
            + columns[2]
            + " FLOAT,\n"
            + columns[3]
            + " INTEGER,\n"
            + columns[4]
            + " FLOAT,\n"
            + columns[5]
            + " INTEGER,\n"
            + columns[6]
            + " FLOAT,\n"
            + columns[7]
            + " INTEGER,\n"
            + columns[8]
            + " VARCHAR(10),\n"
            + columns[9]
            + " VARCHAR(50));"
        )
        cursor.execute(sql_cmd)
        self.conn.commit()
        master_file.close()
        self.__close_cursor(cursor)

    # -------------------------------
    # Copy data from CSV files created in smogon_pull.py into database
    # -------------------------------.
    def fill_tables(self):
        cursor = self.create_cursor();
        master_file = open(self.__FILE, "r")
        columns = tuple(master_file.readline().strip().split(","))
        cursor.copy_from(master_file, self.table_name, columns=columns, sep=",")
        self.conn.commit()
        master_file.close()
        self.__close_cursor(cursor)
        print("Tables updated with new data.")

    # -------------------------------
    # Disconnect from database.
    # -------------------------------
    def close_connection(self):
        self.conn.close()
        print("Connection to database closed.")

    # -------------------------------
    # Pokedex builder
    # -------------------------------
    def pokedex(self):
        j = open(r"C:\dev\python\smog_usage_stats\data\reference\pokedex.json")
        dex = json.load(j)

        cursor = self.create_cursor();
        columns = list(dex["data"]["bulbasaur"].keys())
        query = "DROP TABLE IF EXISTS branchdex; CREATE TABLE branchdex ( "
        query += (
            "id SERIAL PRIMARY KEY,"
            f"{columns[0]} INTEGER, {columns[1]} VARCHAR(16),"
            f"{columns[2]} VARCHAR(50), {columns[3]} VARCHAR(50),"
            f"{columns[4]} VARCHAR(50), {columns[5]} VARCHAR(50),"
            f"{columns[6]} VARCHAR(50), {columns[7]} VARCHAR(50),"
            f"{columns[8]} VARCHAR(50), {columns[9]} VARCHAR(50),"
            f"{columns[10]} VARCHAR(50), {columns[11]} INTEGER,"
            f"{columns[12]} INTEGER, {columns[13]} INTEGER,"
            f"{columns[14]} INTEGER, {columns[15]} INTEGER,"
            f"{columns[16]} INTEGER, {columns[17]} INTEGER);"
        )

        cursor.execute(query)
        j.close()
        
        pokemon = tuple(dex["data"].keys())
        values = []
        for p in pokemon:
            values.append(tuple(dex["data"][p][col] for col in columns))

        for val in values:
            insert_stmt = "INSERT INTO branchdex ({}) values {};".format(
                ", ".join([c for c in columns]), val
            )
            print(insert_stmt)
            cursor.execute(insert_stmt)
        self.conn.commit();
        self.__close_cursor(cursor)
        print("created pokedex table")

        # print(dex)


if __name__ == "__main__":
    SqlManager = SQLManager()
    SqlManager.connect(db_name="UsageStats")
    SqlManager.pokedex()
    # SqlManager.construct_tables()
    # SqlManager.fill_tables()
    SqlManager.close_connection()

import os
import zipfile
import psycopg2 as pg2
from os.path import join, dirname
from dotenv import load_dotenv

# TODOS:
# 1 Create JSON input option. Mostly just to do it, and because 
#   I find myself using a lot of JSON lately, 
#   and having to use pandas is really fucking heavy.
#
# 2 Probably should make the database more optimal, 
#   but I don't even know if anyone uses this.  

# -------------------------------
# Connection variables
# -------------------------------
dotenv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.env')) #travels up a level to find the .env
load_dotenv(dotenv_path)

# -------------------------------
# Connection to database
# -------------------------------
# Server connection
# db_url = os.environ.get("DATABASE_URL")
# CONN = pg2.connect(db_url, sslmode="require")
# print("Connected remotely.")

# Local connection
CONN = pg2.connect(
    database = os.environ.get('LOCAL_DATABASE'),
    user     = os.environ.get('LOCAL_USER'),
    password = os.environ.get('LOCAL_PASSWORD'),
    host     = os.environ.get('LOCAL_HOST'),
    port     = os.environ.get('LOCAL_PORT')
)
print("Connected locally.")

print("Connected to PG!")
CUR = CONN.cursor()

# -------------------------------
# Database manager class
# -------------------------------
class DB_Manager:
    def __init__(self):
        self.table_name = "smogon_usage_stats"
        try: 
            self.__FILE = os.path.join(
                os.getcwd(), 
                "data/statsmaster.csv"
                )
        except:
            print('you haven\'t downloaded any stats')

    # -------------------------------
    # Create the tables for the database
    # -------------------------------
    # def construct_tables(self):
    def construct_tables(self):
        master_file = open(self.__FILE)
        columns = master_file.readline().strip().split(",")

        sql_cmd = "DROP TABLE IF EXISTS " + self.table_name + ";\n"
        sql_cmd += "CREATE TABLE " + self.table_name + " (\n"

        sql_cmd += (
            "id_ SERIAL PRIMARY KEY,\n"
            + columns[0] + " INTEGER,\n"
            + columns[1] + " VARCHAR(50),\n"
            + columns[2] + " FLOAT,\n"
            + columns[3] + " INTEGER,\n"
            + columns[4] + " FLOAT,\n"
            + columns[5] + " INTEGER,\n"
            + columns[6] + " FLOAT,\n"
            + columns[7] + " INTEGER,\n"
            + columns[8] + " VARCHAR(10),\n"
            + columns[9] + " VARCHAR(50));"
        )
        CUR.execute(sql_cmd)
        CONN.commit()
        master_file.close()

    # def construct_tables_json(self):
    #     if self.__FILE.endswith('.json'):
            
    #     else:
    #       return "Error: Please use `construct_tables_CSV` or generate a JSON file of data."
    # -------------------------------
    # Copy data from CSV files created in smogon_pull.py into database
    # -------------------------------.
    def fill_tables(self):

        master_file = open(self.__FILE, "r")
        columns = tuple(master_file.readline().strip().split(","))
        CUR.copy_from(
            master_file,
            self.table_name,
            columns=columns,
            sep=","
        )
        CONN.commit()
        master_file.close()
        print("Tables updated with new data.")
    # -------------------------------
    # Disconnect from database.
    # -------------------------------
    def close_db(self):
        CUR.close()
        print("Cursor closed.")
        CONN.close()
        print("Connection to server closed.")

if __name__ == "__main__":

    manager = DB_Manager()
    print("connected")
    manager.construct_tables()
    print("table made")
    manager.fill_tables()
    print("filled")
    manager.close_db()
    
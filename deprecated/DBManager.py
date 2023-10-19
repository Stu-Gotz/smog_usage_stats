import os
import psycopg2 as pg2
from os import path
from dotenv import load_dotenv
import json
import datetime
from dateutil.relativedelta import relativedelta
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
dotenv_path = path.abspath(
    path.join(path.dirname(__file__), "..", ".env")
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
        self.__dirs = ('current', 'previous', 'tma')
        self.__path = self.__set_path_variable();
    
    def __set_path_variable(self):
        dirpath = path.join(os.getcwd(), 'data')
        print(dirpath)
        return dirpath

    # This function exists to allow modification of db connection variables and establish a connection
    # mostly because my credentials are different on my desktop and laptop, but also makes it flexible
    # for other people to use, as its open source software, might as well make it easy.
    def connect(self, 
                db_name=False, 
                user_name=False, 
                pwd=False, 
                hostname=False, 
                port_num=False
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
            self.conn = self.connect()
        curr = conn.cursor()
        return curr
    
    def __close_cursor(self, cursor):
        cursor.close()

    def set_dates(self):
        # Due to the nature of stats collection, it will always be 1 month behind
        # the current month, so we set the current one to one month ago and use
        # the relativedelta() function to get the next two previous months
        # i.e. if it is currently April, current, previous and tma will 
        # be March, Feb and Jan, respectively
        self.current = (datetime.datetime.now() - relativedelta(months=1))
        self.previous = (self.current - relativedelta(months=1)).strftime('%Y-%m')
        self.tma = (self.current - relativedelta(months=2)).strftime('%Y-%m')
        self.current = self.current.strftime('%Y-%m') #change to a string after getting other months
        # print(self.current)
        # print(self.previous)
        # print(self.tma)
    
    # -------------------------------
    # Create the tables for the database
    # -------------------------------
    def construct_tables(self):
        source_file = open(path.join(self.__path, 'statsmaster.csv'))
        columns = source_file.readline().strip().split(",")

        cursor = self.create_cursor();

        # I'm absolutely sure there is a better way to do this, but 
        # for the sake of this project, I am only keeping a rolling 3 months of data for space-saving
        # constraints and practical reasons (does what was happening 6 months ago influence now? not really
        # when it comes to pokemon)

        columns = (
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
            + " VARCHAR(10),\n"
            + columns[8]
            + " VARCHAR(10),\n"
            + columns[9]
            + " VARCHAR(50)"
        )
        sql_cmd = f"DROP TABLE IF EXISTS {self.__dirs[-1]}; \n"
        sql_cmd += f"ALTER TABLE IF EXISTS {self.__dirs[1]} RENAME TO {self.__dirs[-1]};\n"
        sql_cmd += f"ALTER TABLE IF EXISTS {self.__dirs[0]} RENAME TO {self.__dirs[1]};\n"
        sql_cmd += f"CREATE TABLE {self.__dirs[0]} ({columns});\n"
        sql_cmd += f"CREATE TABLE IF NOT EXISTS {self.__dirs[1]} ({columns});\n"
        sql_cmd += f"CREATE TABLE IF NOT EXISTS {self.__dirs[-1]} ({columns});\n"

        
        cursor.execute(sql_cmd)
        self.conn.commit()
        source_file.close()
        self.__close_cursor(cursor)

    # -------------------------------
    # Copy data from CSV files created in smogon_pull.py into database
    # -------------------------------.
    def fill_table(self, table_name, directory):
        cursor = self.create_cursor();

        for filename in os.listdir(directory):
            with open(path.join(self.__path, '\\'.join([directory, filename])), 'r') as currentfile:
                # print(currentfile)
                columns = tuple(currentfile.readline().strip().split(","))
                cursor.copy_from(currentfile, table_name, columns=columns, sep=",")
                self.conn.commit()
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
    def create_pokedex_table(self):
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
            # print(insert_stmt)
            cursor.execute(insert_stmt)
        self.conn.commit();
        self.__close_cursor(cursor)
        print("created pokedex table")

        # print(dex)

    def update_tables(self):
        self.construct_tables()
        for d in self.__dirs:
            self.fill_table(d, path.join(self.__path, d))
        self.close_connection()
        return

if __name__ == "__main__":

    SqlManager = SQLManager()
    SqlManager.connect(db_name="UsageStats")
    SqlManager.update_tables()
    # # SqlManager.pokedex()
    # # SqlManager.fill_tables()
    # SqlManager.close_connection()
    # today = (datetime.datetime.now() - relativedelta(months=1))
    # thismonth = (today - relativedelta(months=1)).strftime('%Y-%m')
    # print(thismonth)
    # for f in os.listdir(r"C:\dev\python\smog_usage_stats\data\csv"):
    #     if f.startswith(thismonth):
    #         print(f)
    # print(os.getcwd())
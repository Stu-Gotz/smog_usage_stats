import os
import zipfile
import psycopg2 as pg2

# -------------------------------
# Connection variables
# -------------------------------
USER = "postgres"
PASSWORD = "password"
DATABASE = "usagestats"
HOST = "127.0.0.1"
PORT = "5432"

# -------------------------------
# Connection to database
# -------------------------------
try:
    CONN = pg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )

    print("Connected to POSTGRES!")
    CUR = CONN.cursor()
except pg2.OperationalError:
    print("Something isn't quite correct. Check database or connection variables.")

# -------------------------------
# Database manager class
# -------------------------------
class DB_Manager:
    def __init__(self):
        self.table_name = "smogon_usage_stats"
        self.__FILE = os.path.join(os.getcwd(), "data/statsmaster.csv")

    # -------------------------------
    # Create the tables for the database
    # -------------------------------
    def construct_tables(self):

        # # Input should be in format %YYYY_%DD_%Rating ex: 2020_03_1760
        # zf = zipfile.ZipFile(self.__FILE)
        master_file = open(self.__FILE)
        columns = master_file.readline().strip().split(",")

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

        CUR.execute(sql_cmd)
        CONN.commit()

    # -------------------------------
    # Copy data from CSV files created in smogon_pull.py into database
    # -------------------------------.
    def fill_tables(self):

        master_file = open(self.__FILE, "r")
        columns = tuple(master_file.readline().strip().split(","))
        CUR.copy_from(master_file, self.table_name, columns=columns, sep=",")
        CONN.commit()

    # -------------------------------
    # Disconnect from database.
    # -------------------------------
    def close_db(self):
        CUR.close()
        print("Cursor closed.")
        CONN.close()
        print("Connection to server closed.")


if __name__ == "__main__":

    # print("hello")
    # __dir = os.getcwd()
    # __dir = os.path.join(__dir, "data/csv")
    # print(__dir)

    # dirlist = os.listdir(__dir)
    # print(dirlist)
    manager = DB_Manager()
    print("connected")
    # datelist = []
    manager.construct_tables()
    print("table made")
    manager.fill_tables()
    print("filled")
    # manager.close_db()
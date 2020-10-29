import psycopg2 as pg2
import os

# -------------------------------
# Connection variables
# -------------------------------
USER = "postgres"
PASSWORD = "password"
DATABSE = "usagestats"
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
except psycopg2.OperationalError:
    print("Something isn't quite correct. Check database or connection variables.")

# -------------------------------
# Database manager class
# -------------------------------
class DB_Manager:
    def __init__(self, dirlist):
        self.__path = os.getcwd()
        self._path = os.path.join(os.getcwd(), "data/csv/")
        self.dirlist = dirlist

    # -------------------------------
    # Create the tables for the database
    # -------------------------------
    def construct_tables(self):

        # # Input should be in format %YYYY_%DD_%Rating ex: 2020_03_1760

        for d in self.dirlist:
            fileInput = open(os.path.join(self._path, d), "r")
            columns = fileInput.readline().strip().split(",")

            table_name = d.replace("-", "_").replace(".csv", "").replace(".json", "")
            sql_cmd = "DROP TABLE IF EXISTS usage_" + table_name + ";\n"
            sql_cmd += "CREATE TABLE usage_" + table_name + " (\n"

            sql_cmd += (
                columns[0]
                + " INTEGER,\n"
                + columns[1]
                + " VARCHAR(50) PRIMARY KEY,\n"
                + columns[2]
                + " FLOAT,\n"
                + columns[3]
                + " INTEGER,\n"
                + columns[4]
                + " FLOAT,\n"
                + columns[5]
                + " INTEGER,\n"
                + columns[6]
                + " FLOAT);"
            )

            CUR.execute(sql_cmd)
        CONN.commit()

    # -------------------------------
    # Copy data from CSV files created in smogon_pull.py into database
    # -------------------------------.
    def fill_tables(self):

        for d in self.dirlist:
            fileInput = open(os.path.join(self._path, d), "r")
            columns = tuple(fileInput.readline().strip().split(","))

            # f = open(, "r")
            filepath = os.path.join(self._path, d)
            table_name = "usage_" + d.replace("-", "_").replace(".csv", "").replace(
                ".json", ""
            )
            CUR.copy_from(fileInput, table_name, columns=columns, sep=",")

        CONN.commit()

    # -------------------------------
    # Disconnect from database.
    # -------------------------------
    def close_db(self):
        CUR.close()
        print("Cursor closed.")
        CONN.close()
        print("Connection to server closed.")


# if __name__ == "__main__":

#     print("hello")
#     __dir = os.getcwd()
#     __dir = os.path.join(__dir, "data/csv")
#     print(__dir)

#     dirlist = os.listdir(__dir)
#     print(dirlist)
#     manager = DB_Manager(dirlist)
#     print("connected")
#     # datelist = []
#     manager.construct_tables()
#     print("table made")
#     manager.fill_tables()
#     print("filled")
#     manager.close_db()
import os
import psycopg2
from dotenv import load_dotenv
from os.path import dirname as up

try:
    load_dotenv()
except:
    print("No local environment variables found.")


_COLUMNS = (
    "rank",
    "pokemon",
    "usage_pct",
    "raw_usage",
    "raw_pct",
    "real",
    "real_pct",
    "date",
    "tier"
)


class SQLInterface:
    def __init__(
        self,
        db_name: str = None,
        username: str = None,
        pwd: str = None,
        host: str = None,
        port: str = None,
    ) -> None:
        self.db_name = db_name
        self.username = username
        self.pwd = pwd
        self.host = host
        self.port = port
        self.conn = self.connect(db_name, username, pwd, host, port)
        # self.cur = self.conn.cursor() if self.conn else None

    def connect(
        self,
        database: str = None,
        user: str = None,
        password: str = None,
        host: str = None,
        port: str = None,
    ) -> psycopg2.extensions.connection:
        """
        
        """
        connection = psycopg2.connect(
            database=database if database else os.environ.get("LOCAL_DATABASE"),
            user=user if user else os.environ.get("LOCAL_USER"),
            password=password if password else os.environ.get("LOCAL_PASS"),
            host=host if host else os.environ.get("LOCAL_HOST"),
            port=port if port else os.environ.get("LOCAL_PORT"),
        )

        if connection:
            self.conn = connection
            print("connected")
        else:
            raise ConnectionError("No database connection was established. Please check your credentials.")
        return connection

    def _create_cursor(self) -> psycopg2.extensions.cursor:
        """
        If the user hasn't connected manually, no self.conn exists, so we must call it and create the cursor from default values.

        This function is here because its good practice to close the cursor after executing a command. So it is called at the top of a
        SQL-performing function and closed after it.
        """
        if not self.conn:
            self.conn = self.connect()
        curr = self.conn.cursor()
        return curr

    def update_tables(self) -> None:
        db_names = ("current", "previous", "tma")
        columns = (
            "id_ SERIAL PRIMARY KEY,\n"
            + _COLUMNS[0]
            + " INTEGER,\n"
            + _COLUMNS[1]
            + " VARCHAR(50),\n"
            + _COLUMNS[2]
            + " FLOAT,\n"
            + _COLUMNS[3]
            + " INTEGER,\n"
            + _COLUMNS[4]
            + " FLOAT,\n"
            + _COLUMNS[5]
            + " INTEGER,\n"
            + _COLUMNS[6]
            + " FLOAT, \n"
            + _COLUMNS[7]
            + " VARCHAR(50), \n"
            + _COLUMNS[8]
            + " VARCHAR(50)"
        )

        cursor = self._create_cursor()

        sql_cmd = f"DROP TABLE IF EXISTS {db_names[-1]}; \n"
        sql_cmd += f"DROP TABLE IF EXISTS {db_names[1]};\n"
        sql_cmd += f"DROP TABLE IF EXISTS {db_names[0]};\n"
        sql_cmd += f"CREATE TABLE {db_names[0]} ({columns});\n"
        sql_cmd += f"CREATE TABLE {db_names[1]} ({columns});\n"
        sql_cmd += f"CREATE TABLE {db_names[-1]} ({columns});\n"

        cursor.execute(sql_cmd)
        self.conn.commit()
        self._close_cursor(cursor)
        return

    def load_data_to_table(self, target_table: str) -> None:
        cursor = self._create_cursor()

        target_dir = os.path.abspath(
            os.path.join(
                f"{up(up(__file__))}\\data\\", target_table
            )
        )

        print(target_dir)
        for source in os.listdir(target_dir):
            with open(os.path.join(target_dir, source), "r") as truth:
                next(truth)
                cursor.copy_from(truth, target_table, columns=_COLUMNS, sep=",")
                self.conn.commit()
        self._close_cursor(cursor)

    def close_connection(self) -> None:
        """Closes database connection."""
        self.conn.close()

    def _close_cursor(self, cursor: psycopg2.extensions.cursor) -> None:
        """Closes cursor."""
        cursor.close()

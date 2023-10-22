import os
import psycopg2
from dotenv import load_dotenv

try:
    load_dotenv()
except:
    pass

_COLUMNS = (
    "rank",
    "pokemon",
    "usage_pct",
    "raw_usage",
    "raw_pct",
    "real",
    "real_pct",
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
        self.cur = self.conn.cursor() if self.conn else None

    def connect(self):
        connection = psycopg2.connect(
            database=self.dbname if self.db_name else os.environ.get("LOCAL_DATABASE"),
            user=self.username if self.username else os.environ.get("LOCAL_USER"),
            password=self.pwd if self.pwd else os.environ.get("LOCAL_PASSWORD"),
            host=self.host if self.host else os.environ.get("LOCAL_HOST"),
            port=self.port_num if self.port else os.environ.get("LOCAL_PORT"),
        )

        if connection:
            self.conn = connection
            print("connected")
        else:
            print("error")
        return connection

    def create_cursor(self) -> psycopg2.extensions.cursor:
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
            + " FLOAT"
        )

        cursor = self.create_cursor()

        sql_cmd = f"DROP TABLE IF EXISTS {db_names[-1]}; \n"
        sql_cmd += f"ALTER TABLE IF EXISTS {db_names[1]} RENAME TO {db_names[-1]};\n"
        sql_cmd += f"ALTER TABLE IF EXISTS {db_names[0]} RENAME TO {db_names[1]};\n"
        sql_cmd += f"CREATE TABLE {db_names[0]} ({columns});\n"
        sql_cmd += f"CREATE TABLE IF NOT EXISTS {db_names[1]} ({columns});\n"
        sql_cmd += f"CREATE TABLE IF NOT EXISTS {db_names[-1]} ({columns});\n"

        cursor.execute()
        self.conn.commit()
        self.close_cursor(cursor)
        return

    def load_data_to_table(self, target_table: str, source: str | os.PathLike) -> None:
        cursor = self.create_cursor()

        source = os.path.join(os.path.dirname(os.path.dirname(__file__)), source)
        with open(source) as truth:
            next(truth)
            cursor.copy_from(truth, target_table, columns=_COLUMNS, sep=",")
            self.conn.commit()
        self.close_cursor(cursor)

    def close_connection(self) -> None:
        """Closes database connection."""
        self.conn.close()

    def close_cursor(cursor: psycopg2.extensions.cursor) -> None:
        """Closes cursor."""
        cursor.close()

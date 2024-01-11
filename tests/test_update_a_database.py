from smog_usage_stats import UsageStatsLookup, IndividualLookup
# old Update.py, moved to testing because its not really in the spirit of what i want for the package. 
# from UsageStatsLookup import BaseStatsSearch, MonotypeStatsSearch
# from IndividualLookup import BaseChaosSearch, MonotypeChaosSearch
# from SQLInterface import SQLInterface
# from Search import Search
import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup
import psycopg2
import os

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

# param_dict something like


# {
#   branch: 'BaseStats', 'MonoStats', 'BaseChaos', 'MonoChaos"
#   year, gen, month, tier or typing all as their own fields
#   isMonotype: True or False
#   }
class Updater:
    @staticmethod
    def _set_query_object(param_dict: dict):# -> Search.Search:
        """
        Basically a backend router that returns a Search.<subclass> object
        """
        match param_dict["branch"]:
            case "BaseStats":
                new_query = UsageStatsLookup.BaseStatsSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    tier=param_dict["branch_param"],
                )
                return new_query
            case "MonoStats":
                new_query = UsageStatsLookup.MonotypeStatsSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    typing=param_dict["branch_param"],
                )
            case "BaseChaos":
                new_query = IndividualLookup.BaseChaosSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    tier=param_dict["branch_param"],
                )
            case "MonoChaos":
                new_query = IndividualLookup.MonotypeChaosSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    typing=param_dict["branch_param"],
                )
        return new_query

    @staticmethod
    def _update_database() -> None:
        """Updates the database with new data."""
        sqli = SQLInterface()
        sqli.connect()
        sqli.update_tables()
        for i in ("current", "previous", "tma"):
            sqli.load_data_to_table(i)

        sqli.close_connection()
        print("Database successfully updated.")

    def update_monthly(self) -> None:
        """Called on a monthly basis to update the database as new stats are released."""
        today = datetime.now()

        # realistically, I should only have to need the current data, and then I can
        # just reshuffle the folders with shutil functions, which I will probably
        # change to, but I need to get a working amount of data to work with and have
        # something to fall back on if I somehow delete a bunch of data I cannot get
        # back.
        # I kind of already did this in the old version, so I'll just look there and
        # see how to handle it.
        date_dict = {
            "current": today - relativedelta(months=1),
            "previous": today - relativedelta(months=2),
            "tma": today - relativedelta(months=3),
        }

        gens = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        def get_tiers(date_obj: datetime) -> tuple[str]:
            """Internal function to get the available tiers to query. Faster than
            iterating as it reduces the number of tiers by only picking from the
            available ones. There's definitely a better way to do this which I am
            going to change to that just uses the anchor tags ending in -1500.txt,
            but at the moment this is good enough for a solution to work on perfecting.

                Params:
                date_object (datetime): a datetime object of at least YYYY-MM format

                Returns:
                tuple[str] -> a tuple of tiers, as string values
            """
            year = date_obj.strftime("%Y")
            month = date_obj.strftime("%m")
            url = f"https://www.smogon.com/stats/{year}-{month}/"

            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            anchors = soup.find_all("a")
            available_tiers = []
            for a in anchors[6:]:
                a = a.text.strip("gen")
                a = a.split("-")[0]
                for g in gens:
                    if a.startswith(g):
                        a = a[1:]
                        print(a)
                available_tiers.append(a)
            return tuple(set(available_tiers))

        def get_data(date_obj: datetime, table: str, isMonotype: bool = False) -> None:
            tiers = get_tiers(date_obj)
            for g in gens:
                for t in tiers:
                    print(
                        date_dict[table].strftime("%Y"),
                    )
                    q = self._set_query_object(
                        {
                            "year": date_dict[table].strftime("%Y"),
                            "month": date_dict[table].strftime("%m"),
                            "gen": g,
                            "branch_param": t,
                            "branch": "BaseStats",
                            "isMonotype": isMonotype,
                        }
                    )
                    print(q.base)
                    q.search_and_save(pathname=table)

        for k in date_dict.keys():
            get_data(date_dict[k], k)

        self._update_database()



assert Updater().update_monthly()

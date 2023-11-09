import UsageStatsLookup as StatsSearch
import IndividualLookup as IndividualSearch
from SQLInterface import SQLInterface
from Search import Search
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from bs4 import BeautifulSoup

# param_dict something like


# {
#   branch: 'BaseStats', 'MonoStats', 'BaseChaos', 'MonoChaos"
#   year, gen, month, tier or typing all as their own fields
#   isMonotype: True or False
#   }
class Updater:
    @staticmethod
    def _set_query_object(param_dict: dict) -> Search:
        """
        Basically a backend router that returns a Search.<subclass> object
        """
        match param_dict["branch"]:
            case "BaseStats":
                new_query = StatsSearch.BaseStatsSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    tier=param_dict["branch_param"],
                )
                return new_query
            case "MonoStats":
                new_query = StatsSearch.MonotypeStatsSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    typing=param_dict["branch_param"],
                )
            case "BaseChaos":
                new_query = IndividualSearch.BaseChaosSearch(
                    year=param_dict["year"],
                    month=param_dict["month"],
                    gen=param_dict["gen"],
                    tier=param_dict["branch_param"],
                )
            case "MonoChaos":
                new_query = IndividualSearch.MonotypeChaosSearch(
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


# Updater().update_monthly()
# Updater._update_database()

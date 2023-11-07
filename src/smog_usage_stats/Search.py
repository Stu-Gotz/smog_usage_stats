from typing import Literal
from os.path import dirname as up
import os
import shutil
from datetime import datetime
from bs4 import BeautifulSoup
import csv


# "Mega"-parent searching class. Everything contained within this class will be available,
# but not necessarily used by child classes.
class Search:
    """Parent searcher class.

    ::params:
    >year (str or int): a string or integer year
    >month (str): two-digit string month
    >gen: (str or int): an integer for whichever Pokemon generation is being queried."""

    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        self.year = year
        self.month = month
        self.date = datetime.strptime(("-".join([str(year), month])), "%Y-%m")
        self.gen = gen
        self.base = "https://www.smogon.com/stats/"

    @property
    def year(self) -> str | int:
        return self._year

    @property
    def month(self) -> str:
        return self._month

    @property
    def gen(self) -> str:
        return self._gen

    @gen.setter
    def gen(self, value):
        self._gen = value

    @year.setter
    def year(self, value):
        self._year = value

    @month.setter
    def month(self, value):
        self._month = value

    def _save_output(
        self,
        data: list[list],
        ending: str,
        pathname: str | os.PathLike = None,
    ) -> None:
        if pathname:
            storage_dir = os.path.join(
                f"{self.locate_base_data_directory()}/", pathname
            )
        else:
            storage_dir = os.path.join(f"{self.locate_base_data_directory()}/cache")

        if not os.path.exists((storage_dir)):
            os.mkdir(storage_dir)
        # make the document
        filepath = os.path.join(storage_dir, f"{self.year}-{self.month}_{ending}.csv")
        with open(
            filepath,
            "w",
            newline="",
        ) as file:
            csvWriter = csv.writer(file, delimiter=",")
            csvWriter.writerows(data)

        if os.stat(filepath).st_size < 100:
            os.remove(filepath)
            print(f"File {filepath} deleted as it contained no data.")

    def search_and_save(self, pathname: str | os.PathLike = None) -> None:
        """
        Searches the smogon stats repo and saves files to system.
        """
        data = self.search()
        if self.ending:
            ending = self.ending.split("-")[0]
            self._save_output(data, ending, pathname=pathname)
        else:
            print("No data was saved.")
            return None

    def create_validation_object(self):
        this = vars(self)
        validation_object = {k.replace("_", ""): v for k, v in this.items()}
        return validation_object

    def locate_base_data_directory(self, reference: str | os.PathLike) -> os.PathLike:
        """"""
        base_dir = up(up(reference))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data")
        return cache_dir

    @staticmethod
    def clear_cache() -> None:
        """Clears cache files if there are any."""
        base_dir = up(up(__file__))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

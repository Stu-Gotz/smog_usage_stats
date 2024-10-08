from typing import Literal
from os.path import dirname as up
import os
import shutil
from datetime import datetime
import csv


# "Mega"-parent searching class. Everything contained within this class will be available,
# but not necessarily used by child classes.
class _Search:
    """Parent searcher class.

    ::params:
    >year (str or int): a string or integer year
    >month (str): two-digit string month
    >gen: (str or int): an integer for whichever Pokemon generation is being queried."""

    def __init__(
        self,
        year: str | int,
        month: str,
        gen: str | int,
    ) -> None:
        self.year = year
        self.month = month
        self.gen = gen
        self.base = f"https://www.smogon.com/stats/{year}/{month}/"
        self.isMonotype = False

    def __str__(self):
        return self.base
    
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
        self._gen = int(value)

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
        pathname: str | os.PathLike = None
    ) -> None:
        if pathname:
            storage_dir = f"{os.getcwd()}\\" + pathname
        else:
            storage_dir = f"{os.getcwd()}\\" + "cache"

        if not os.path.exists((storage_dir)):
            os.makedirs(storage_dir)
        # make the document
        filepath = os.path.join(storage_dir, f"{self.year}-{self.month}_{ending}.csv")
        with open(filepath, "w",newline="") as file:
            csvWriter = csv.writer(file, delimiter=",")
            csvWriter.writerows(data)

        if os.stat(filepath).st_size < 100:
            os.remove(filepath)
            print(f"File {filepath} deleted as it contained no or very little data.")

    def search_and_save(self, pathname: str | os.PathLike = None) -> None:
        """
        Searches the smogon stats repo and saves files to system.

            Params:
            pathname: str | os.PathLike -> (Optional) string or os.PathLike
            object for a directory to save the data. If left None will create a
            data directory in the project folder.

            Returns:
            None if saving fails.
        """
        data = self.search()
        if self.ending:
            ending = self.ending.split("-")[0]
            self._save_output(data, ending, pathname=pathname)
        else:
            print("No data was saved.")
            return None

    def _create_validation_object(self):
        this = vars(self)
        validation_object = {k.replace("_", ""): v for k, v in this.items()}
        return validation_object

    # def _locate_base_data_directory(
    #     self
    # ) -> os.PathLike:
    #     """"""
    #     base_dir = up(up(up(".")))
    #     # set up the cached dir, theres probably a better way to do this but for now it will suffice
    #     cache_dir = os.path.join(base_dir, "data")
    #     return cache_dir

    def _set_target_dir(self, target_dir: str):
        return target_dir
    
    @staticmethod
    def clear_cache() -> None:
        """Clears cache files if there are any."""
        base_dir = up(up("."))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
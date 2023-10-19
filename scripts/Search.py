from typing import Literal
from os.path import dirname as up
import os
import shutil

class Search:
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        self.year = year
        self.month = month
        self.gen = gen

    @property
    def year(self) -> str | int:
        return self._years

    @property
    def month(self) -> str:
        return self._months

    @property
    def gen(self) -> str | int:
        return self._gens

    @year.setter
    def year(self, value):
        self._years = value

    @month.setter
    def month(self, value):
        self._months = value

    @gen.setter
    def gen(self, value):
        self._gens = value

    def remove_formatting(self, data: list) -> list[list]:
            # Set the column names first
            outlist = [
                [
                    "rank",
                    "pokemon",
                    "usage_pct",
                    "raw_usage",
                    "raw_pct",
                    "real",
                    "real_pct",
                ]
            ]
            # Remove the formatting from the webpage
            for line in data:
                # remove all linebreaks,symbols and make lowercase
                line = line.strip("\n")
                line = line.replace("|", ",").replace(" ", "").replace("%", "").lower()
                if line.startswith(","):
                    # remove leading and trailing commas
                    line = line[1:-1]
                    # turns it from a list of strings toa 2-d array
                    line = line.split(",")
                    # add it to the list to be returned
                    outlist.append(line)
            return outlist
    
    def locate_cache_dir(self, reference):
        base_dir = up(up(reference))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        return cache_dir
    
    @staticmethod
    def clear_cache():
        base_dir = up(up(__file__))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
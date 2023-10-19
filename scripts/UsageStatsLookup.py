from typing import Literal
from Search import Search
import requests
import csv
import os
from os.path import dirname as up
import shutil


class StatsSearch(Search):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        super().__init__(year, month, gen)

    def search(self) -> list[list]:
        
        # send the request to get the data
        res = requests.get(self.base)
        #get the text if there is any (should add a check in here)
        data = res.text
        #send each "unit" of information to a list by splitting on linebreaks
        data = data.split("\n")
        #truncate to get rid of the non-relevant prefixes and last two lines of styling
        data = data[5:-2]
        #remove the formatting
        data = self.remove_formatting(data)
        
        return data

    def save_output(self, data) -> None:
        cache_dir = self.locate_cache_dir(__file__)

        if not os.path.exists((cache_dir)):
            os.mkdir(cache_dir)
        # make the document    
        with open(
            os.path.join(
                cache_dir, f"{self.year}-{self.month}_gen{self.gen}{self.tier}.csv"
            ),
            "w",
            newline="",
        ) as file:
            csvWriter = csv.writer(file, delimiter=",")
            csvWriter.writerows(data)

class BaseStatsSearch(StatsSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        tier: str,
    ) -> None:
        super().__init__(year, month, gen)
        self.tier = tier.lower()
        self.base = f"https://www.smogon.com/stats/{self.year}-{self.month}/"

    @property
    def tier(self) -> str:
        return self._tier

    @tier.setter
    def tier(self, value):
        self._tier = value

    def build_url(self):
        rating = 1630

        if self.tier == "ou":
            rating = 1695

        self.base += f"gen{self.gen}{self.tier}-{rating}.txt"


class MonotypeStatsSearch(StatsSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        typing: str,
    ) -> None:
        super().__init__(year, month, gen)
        self.typing = typing
        self.base = "https://www.smogon.com/stats/2022-11/monotype/"

    @property
    def typing(self) -> str:
        return self._typing

    @typing.setter
    def typing(self, value):
        self._typing = value

    def build_url(self):
        self.base += f"gen{self.gen}monotype-mono{self.typing}-1500.txt"


if __name__ == "__main__":
    search = BaseStatsSearch(2022, "08", 8, "ou")
    search.build_url()
    query = search.search()
    search.save_output(query)
    search.clear_cache()

    pass

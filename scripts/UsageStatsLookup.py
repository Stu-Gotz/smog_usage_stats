from typing import Literal
from Search import Search
import requests
import csv

class StatsSearch(Search):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        super().__init__(year, month, gen)

    def search(self) -> list[list]:
        def remove_formatting(page: list) -> list[list]:
            outlist = []
            # Remove the formatting from the webpage
            for line in data:
                # remove all symbols and make lowercase
                line = line.replace("|", ",").replace(" ", "").replace("%", "").lower() 
                if line.startswith(","):
                    # remove leading and trailing commas
                    line = line[1:-1]
                    #turns it from a list of strings toa 2-d array
                    line = line.split(',')
                    # add it to the list to be returned
                    outlist.append(line)
            return outlist

        res = requests.get(self.base)
        data = res.text
        data = data.split("\n")
        data = remove_formatting(data[5:-2])
        return data

    def save_output(self):

        return

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
    print(query)

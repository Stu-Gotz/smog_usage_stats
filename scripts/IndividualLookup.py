import os
import time
import json
import urllib.request
from datetime import datetime
from typing import Literal


# We will be doing this a lot so make it a function.
def lower_keys(dictionary: dict) -> dict:
    """
    Returns a dictionary with all keys lower-cased.
    """
    return {k.lower(): v for k, v in dictionary.items()}


class ChaosSearch:
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ):
        self.year = year
        self.month = month
        self.gen = gen

    @property
    def year(self):
        return self._years

    @property
    def month(self):
        return self._months

    @property
    def gen(self):
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

    def search(self, pokemon):
        with urllib.request.urlopen(self.base) as u:
            page = u.read()
            page_object = json.loads(page)
            page_object = page_object["data"]
            page_object = lower_keys(page_object)

            try:
                lookup = page_object[pokemon.lower()]
                return lookup
            except:
                return None

class BaseChaosSearch(ChaosSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
        tier: str,
    ):
        super().__init__(year, month, gen)
        self.tier = tier.lower()
        self.base = f"https://www.smogon.com/stats/{self.year}-{self.month}/chaos/"

    @property
    def tier(self):
        return self._tiers

    @tier.setter
    def tier(self, value):
        self._tiers = value

    def build_url(self):
        rating = 1630

        if self.gen == "ou":
            rating = 1695

        self.base += f"gen{self.gen}{self.tier}-{rating}.json"


class MonotypeChaosSearch(ChaosSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
        typing: str,
    ):
        super().__init__(year, month, gen)
        self.base = (
            f"https://www.smogon.com/stats/{self.year}-{self.month}/monotype/chaos/"
        )
        self.typing = typing.lower()

    @property
    def typing(self):
        return self._typing

    @typing.setter
    def typing(self, value):
        self._typing = value

    def build_url(self):
        rating = 1500
        self.base += f"gen{self.gen}monotype-mono{self.typing}-{rating}.json"


if __name__ == "__main__":
    search = BaseChaosSearch("2022", "07", 8, "uu")
    search.build_url()
    result = search.search("SKARMORY")
    print(result)

    monosearch = MonotypeChaosSearch(
        year= 2022,
        month="11",
        gen = 9,
        typing='fairy'
    )
    monosearch.build_url()
    monoresult = monosearch.search("Gardevoir")
    print(monoresult)

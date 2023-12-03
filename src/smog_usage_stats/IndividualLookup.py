import requests
from typing import Literal
from Search import Search
from UsageStatsLookup import BaseStatsSearch

# TODO: Account for rating when gen is current gen to ONLY be 1695, otherwise be 1630


# Chaos searches are basically individual pokemon lookups, where one can get deeper analysis
# such as movesets, held items, EV spreads, etc
class ChaosSearch(Search):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        super().__init__(year, month, gen)

    def search(self, pokemon: str) -> object | None:
        res = requests.get(self.base)
        page_object = res.json()["data"]
        page_object = self.lower_keys(page_object)

        try:
            lookup = page_object[pokemon.lower()]
            return lookup
        except:
            return None

    # We will be doing this a lot so make it a function.
    def lower_keys(self, dictionary: dict) -> dict:
        """
        Returns a dictionary with all keys lower-cased.
        """
        return {k.lower(): v for k, v in dictionary.items()}


class BaseChaosSearch(ChaosSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
        tier: str,
    ) -> None:
        super().__init__(year, month, gen)
        self.tier = tier.lower()
        self.base = f"https://www.smogon.com/stats/{self.year}-{self.month}/chaos/"

    @property
    def tier(self) -> str:
        return self._tier

    @tier.setter
    def tier(self, value):
        self._tier = value

    def build_url(self):
        self.base += f"gen{self.gen}{self.tier}-1500.json"


class MonotypeChaosSearch(ChaosSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
        typing: str,
    ) -> None:
        super().__init__(year, month, gen)
        self.base = (
            f"https://www.smogon.com/stats/{self.year}-{self.month}/monotype/chaos/"
        )
        self.typing = typing.lower()

    @property
    def typing(self) -> str:
        return self._typing

    @typing.setter
    def typing(self, value):
        self._typing = value

    def build_url(self):
        self.base += f"gen{self.gen}monotype-mono{self.typing}-1500.json"


# this is to search stats individually, but its a bit more involved, a WIP
class IndividualStatsSearch(BaseStatsSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        tier: str,
        name: str,
    ) -> None:
        super().__init__(year, month, gen, tier)
        self.name = name.lower()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower()

    def find_individual_usage(self, resmatrix: list[list] = None) -> dict | None:
        # resmatrix is the resulting 2d array from the self.search() function
        if not resmatrix:
            resmatrix = self.search()
        for m in resmatrix:
            if m[1] == self.name:
                return {m[1]: dict(zip(resmatrix[0], m))}
        print("No result found.")
        return None


if __name__ == "__main__":
    # search = BaseChaosSearch("2022", "07", 8, "uu")
    # search.build_url()
    # result = search.search("SKARMORY")
    # print(result)

    # monosearch = MonotypeChaosSearch(year=2022, month="11", gen=9, typing="fairy")
    # monosearch.build_url()
    # monoresult = monosearch.search("Gardevoir")
    # print(monoresult)

    indysearch = IndividualStatsSearch(2022, "11", "8", "ou", "scizor")
    result = indysearch.find_individual_usage()
    print(result)

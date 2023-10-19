import json
import requests
from typing import Literal
from Search import Search

# TODO: Account for rating when gen is current gen to ONLY be 1695, otherwise be 1630


# We will be doing this a lot so make it a function.
def lower_keys(dictionary: dict) -> dict:
    """
    Returns a dictionary with all keys lower-cased.
    """
    return {k.lower(): v for k, v in dictionary.items()}


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
        page_object = res.json()['data']
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
        rating = 1630

        if self.tier == "ou":
            rating = 1695

        self.base += f"gen{self.gen}{self.tier}-{rating}.json"


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
        rating = 1500
        self.base += f"gen{self.gen}monotype-mono{self.typing}-{rating}.json"


if __name__ == "__main__":
    search = BaseChaosSearch("2022", "07", 8, "uu")
    search.build_url()
    result = search.search("SKARMORY")
    print(result)

    monosearch = MonotypeChaosSearch(year=2022, month="11", gen=9, typing="fairy")
    monosearch.build_url()
    monoresult = monosearch.search("Gardevoir")
    print(monoresult)

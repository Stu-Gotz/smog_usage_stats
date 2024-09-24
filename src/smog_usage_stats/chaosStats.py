import requests
from typing import Literal, Optional
from search import Search

# TODO: Account for rating when gen is current gen to ONLY be 1695, otherwise be 1630


# Chaos searches are basically individual pokemon lookups, where one can get deeper analysis
# such as movesets, held items, EV spreads, etc
class ChaosSearch(Search):
    def __init__(
        self,
        year: str | int,
        month: str,
        gen: str | int,
        name: str,
    ) -> None:
        self.name = name.lower()
        super().__init__(year, month, gen)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower()

    def search(self) -> object | None:
        res = requests.get(self.base)
        page_object = res.json()["data"]
        page_object = self.lower_keys(page_object)

        try:
            lookup = page_object[self.name]
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
        month: str,
        gen: str | int,
        name: str,
        tier: str,
    ) -> None:
        super().__init__(year, month, gen, name)
        self.tier = tier.lower()
        self.base = f"https://www.smogon.com/stats/{self.year}-{self.month}/chaos/"
        self._build_url()

    @property
    def tier(self) -> str:
        return self._tier

    @tier.setter
    def tier(self, value):
        self._tier = value

    def _build_url(self):
        self.base += f"gen{self.gen}{self.tier}-1500.json"


class MonotypeChaosSearch(ChaosSearch):
    def __init__(
        self,
        year: str | int,
        month: str,
        gen: str | int,
        name: str,
        typing: str,
    ) -> None:
        super().__init__(year, month, gen, name)
        self.base = (
            f"https://www.smogon.com/stats/{self.year}-{self.month}/monotype/chaos/"
        )
        self.typing = typing.lower()
        self.isMonotype = True
        self._build_url()

    @property
    def typing(self) -> str:
        return self._typing

    @typing.setter
    def typing(self, value):
        self._typing = value

    def _build_url(self):
        self.base += f"gen{self.gen}monotype-mono{self.typing}-1500.json"





# if __name__ == "__main__":
    # search = BaseChaosSearch(year="2022", month="07", gen=8, tier="uu", name="SKARMORY")
    # result = search.search()
    # print(f"{search.name}:  {result}\n")

    # monosearch = MonotypeChaosSearch(
    #     year=2022, month="11", gen=9, typing="fairy", name="Gardevoir"
    # )
    # monoresult = monosearch.search()
    # print(f"{monosearch.name}:  {monoresult}\n")

    # indysearch = IndividualStatsSearch(2022, "11", "8", "ou", "scIzor")
    # indyresult = indysearch.find_individual_usage()
    # print(f"{indysearch.name}:  {indyresult}\n")

    # print(indyresult['rank'])

    # print(result.keys())

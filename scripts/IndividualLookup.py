import requests
from typing import Literal
from Search import Search
from UsageStatsLookup import BaseStatsSearch
from bs4 import BeautifulSoup

# TODO: Account for rating when gen is current gen to ONLY be 1695, otherwise be 1630


# We will be doing this a lot so make it a function.
def lower_keys(dictionary: dict) -> dict:
    """
    Returns a dictionary with all keys lower-cased.
    """
    return {k.lower(): v for k, v in dictionary.items()}

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

#this is to search stats individually, but its a bit more involved, a WIP
class IndividualStatsLookup(BaseStatsSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        tier: str,
    ) -> None:
        super().__init__(year, month, gen, tier)
        
    def build_url(self):
        def vintage_stats(year, month, gen, tier):
            print("checking old urls")
            r = requests.get(f"https://www.smogon.com/stats/{year}-{month}/")
            soup = BeautifulSoup(r.text, "html.parser")
            anchors = soup.find_all("a")

            tiers = set()
            for a in anchors[6:]:
                text = a.text
                text = text.strip(".txt").split("-")[0]
                tiers.add(text)

            if tier in tiers:
                return f"{tier}-1500.txt"
            elif f"gen{gen}{tier}" in tiers:
                return f"gen{gen}{tier}-1500.txt"
            else:
                return "No data available for this tier on this date."

        ###NOTES:
        #   Before 2017-06, there is some weird fuckery with how stats are stored and labeled
        #       Basically no gen6 data before.
        #       lots of tiers without gen{gen}tier prefix (eg: 'ou' 'uu' etc)

        #   Will need:
        #       conditional to check date
        #       method for 2017-06 & before
        #       from there should be same
        #       methods for old and new format should return string for self.base

        if int(self.year) <= 2017:
            if self.month in ["01", "02", "03", "04", "05", "06"]:
                url_to_append = vintage_stats(
                    self.year, self.month, self.gen, self.tier
                )
                print(url_to_append)
                if url_to_append.endswith(".txt"):
                    self.base += url_to_append
                else:
                    raise Exception("Invalid URL")
            else:
                self.base += f"gen{self.gen}{self.tier}-1500.txt"
        print(self.base)


if __name__ == "__main__":
    search = BaseChaosSearch("2022", "07", 8, "uu")
    search.build_url()
    result = search.search("SKARMORY")
    print(result)

    monosearch = MonotypeChaosSearch(year=2022, month="11", gen=9, typing="fairy")
    monosearch.build_url()
    monoresult = monosearch.search("Gardevoir")
    print(monoresult)

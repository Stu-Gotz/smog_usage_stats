import os
import time
import json
import urllib.request
from datetime import datetime


class BaseStatsSearch:
    def __init__(self, year: str, month: str, gen: int, tier: str):
        self.year = year
        self.month = month
        self.gen = gen
        self.tier = tier
        self.base = f"https://www.smogon.com/stats/{self.year}-{self.month}/chaos/"

    @property
    def year(self):
        return self._years

    @property
    def month(self):
        return self._months

    @property
    def gen(self):
        return self._gens

    @property
    def tier(self):
        return self._tiers

    @year.setter
    def year(self, value):
        self._years = value

    @month.setter
    def month(self, value):
        self._months = value

    @gen.setter
    def gen(self, value):
        self._gens = value

    @tier.setter
    def tier(self, value):
        self._tiers = value

    def build_url(self):
        rating = 1630

        if self.gen == "ou":
            rating = 1695

        self.base += f"gen{self.gen}{self.tier}-{rating}.json"

    def search(self):
        with urllib.request.urlopen(self.base) as u:
            page = u.read()
            page_object = json.loads(page)
            return page_object["data"]


class MonotypeStatSearch(BaseStatsSearch):
    def __init__(self):
        super().__init__()
        self.base = "https://www.smogon.com/stats/2022-11/chaos/"


if __name__ == "__main__":
    search = BaseStatsSearch("2022", "07", 8, "uu")
    print(search.build_url())
    result = search.search()
    print(result.keys())

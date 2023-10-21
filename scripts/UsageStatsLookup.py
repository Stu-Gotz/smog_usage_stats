from typing import Literal
from Search import Search
import requests
import csv
import os
from bs4 import BeautifulSoup


class StatsSearch(Search):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        super().__init__(year, month, gen)

    def search(self) -> list[list]:
        print(self.base)
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
    
    
    def vintage_stats(self, year, month, gen, tier):
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
        return self._tier.lower()

    @tier.setter
    def tier(self, value):
        self._tier = value

    def build_url(self):
        #Rating of 1500 is defined by Smogon as their target of a normal player

        #check dates for valid tiers
        #since for now I am only looking up newer stats for database, it will be fine 
        if int(self.year) == 2017:
            if self.month in ["01", "02", "03", "04", "05", "06"]:
                ending = self.vintage_stats(self.year, self.month, self.gen, self.tier)
                print(ending)
                if ending.endswith('.txt'):
                    self.base += ending
        elif int(self.year) < 2017:
            ending = self.vintage_stats(self.year, self.month, self.gen, self.tier)
            print(ending)
            if ending.endswith('.txt'):
                self.base += ending
        else:
            self.base += f'gen{self.gen}{self.tier}-1500.txt' 

class MonotypeStatsSearch(StatsSearch):
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        typing: Literal["Must be string of type, such as 'fighting' or 'psychic'"],
    ) -> None:
        super().__init__(year, month, gen)
        self.typing = typing.lower()
        self.base = "https://www.smogon.com/stats/2022-11/monotype/"

    @property
    def typing(self) -> str:
        return self._typing.lower()

    @typing.setter
    def typing(self, value):
        self._typing = value

    def build_url(self):
        self.base += f"gen{self.gen}monotype-mono{self.typing}-1500.txt"

if __name__ == "__main__":
    search = BaseStatsSearch(2015, "04", 6, "ou")
    search.build_url()
    query = search.search()
    search.save_output(query)
    # search.clear_cache()


    
    pass

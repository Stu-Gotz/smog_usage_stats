from typing import Literal
from Search import Search
import requests
import csv
import os
from bs4 import BeautifulSoup
from Validation import Validations


class StatsSearch(Search):  

    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        super().__init__(year, month, gen)
        self.ending = None

    ### NOT USED IN CHAOS BRANCH SEARCHES ###
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

    def search(self) -> list[list]:
        # send the request to get the data
        res = requests.get(self.base)
        # get the text if there is any (should add a check in here)
        data = res.text
        # send each "unit" of information to a list by splitting on linebreaks
        data = data.split("\n")
        # truncate to get rid of the non-relevant prefixes and last two lines of styling
        data = data[5:-2]
        # remove the formatting
        data = self.remove_formatting(data)

        return data
    
    def search_and_save(self) -> None:
        data = self.search()
        if self.ending:
            ending = self.ending.split('-')[0]
            self.save_output(data, ending)
        else:
            print("No data was saved.")
            return None

    def vintage_stats(self, year, month, gen, tier) -> str:
        r = requests.get(f"https://www.smogon.com/stats/{year}-{month}/")
        soup = BeautifulSoup(r.text, "html.parser")
        anchors = soup.find_all("a")

        tiers = tuple(set(a.text.strip(".txt").split("-")[0] for a in anchors[6:]))

        try:
            print('trying basic')
            if tiers.index(f'gen{gen}{tier}'):
                return f"gen{gen}{tier}-1500.txt"
        except(ValueError):
            print('trying backup')
            try:
                if (tiers.index(tier) and tier == (6 | 7)):
                    return f"{tier}-1500.txt"
            except(ValueError):
                return "Nothing found."


    def save_output(self, data: list[list], ending: str) -> None:
        cache_dir = self.locate_cache_dir(__file__)

        if not os.path.exists((cache_dir)):
            os.mkdir(cache_dir)
        # make the document
        with open(
            os.path.join(
                cache_dir, f"{self.year}-{self.month}_{ending}.csv"
            ),
            "w",
            newline="",
        ) as file:
            csvWriter = csv.writer(file, delimiter=",")
            csvWriter.writerows(data)


class BaseStatsSearch(StatsSearch):
    '''        tier (str): string of tier to be queried.'''
    __doc__ = Search.__doc__ + __doc__
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        tier: str,
    ) -> None:
        super().__init__(year, month, gen)
        self.tier = tier.lower()
        self.base += f"{self.year}-{self.month}/"

    @property
    def tier(self) -> str:
        return self._tier.lower()

    @tier.setter
    def tier(self, value):
        self._tier = value

    def build_url(self):
        # Rating of 1500 is defined by Smogon as their target of a normal player

        validation_object = self.create_validation_object()
        validator = Validations(validation_object)
        # check dates for valid tiers
        # since for now I am only looking up newer stats for database, it will be fine
        if validator.validate():
            if Validations.is_modern_format(validation_object):
                ending = f"gen{self.gen}{self.tier}-1500.txt"
                self.ending = ending
                self.base += ending
            else:
                ending = self.vintage_stats(self.year, self.month, self.gen, self.tier)
                print(ending)
                # below can be deleted after validations are done
                if ending.endswith(".txt"):
                    self.ending = ending
                    self.base += ending
                # else:
                #     raise Exception('Invalid information supplied, check your parameters.')
        else:
            print("Something isn't correct.")


class MonotypeStatsSearch(StatsSearch):
    '''        tier (str): string of tier to be queried.'''
    __doc__ = Search.__doc__ + __doc__
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for Janu…"],
        gen: str | int,
        typing: Literal["Must be string of type, such as 'fighting' or 'psychic'"],
    ) -> None:
        super().__init__(year, month, gen)
        self.typing = typing.lower()
        self.base += f'{year}-{month}/monotype/'

    @property
    def typing(self) -> str:
        return self._typing.lower()

    @typing.setter
    def typing(self, value):
        self._typing = value

    def build_url(self):
        self.base += f"gen{self.gen}monotype-mono{self.typing}-1500.txt"


if __name__ == "__main__":
    search = BaseStatsSearch(2015, "09", 8, "ou")
    search.build_url()
    # query = search.search()
    # search.save_output(query)
    search.search_and_save()
    # search.clear_cache()

    pass

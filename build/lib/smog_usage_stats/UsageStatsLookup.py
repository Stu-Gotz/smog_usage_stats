from typing import Literal
from Search import Search
import requests
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
    def _remove_formatting(self, data: list, isMonotype: bool) -> list[list]:
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
                "date",
                "tier",
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
                line.append(f"{self.year}-{self.month}")
                if not isMonotype:
                    line.append(f"gen{self.gen}{self.tier}")
                elif isMonotype:
                    line.append(f"mono{self.typing}")

                # add it to the list to be returned
                outlist.append(line)
        return outlist

    @staticmethod
    def _vintage_search(year, month, gen, tier) -> str:
        r = requests.get(f"https://www.smogon.com/stats/{year}-{month}/")
        soup = BeautifulSoup(r.text, "html.parser")
        anchors = soup.find_all("a")

        tiers = tuple(set(a.text.strip(".txt").split("-")[0] for a in anchors[6:]))

        try:
            if tiers.index(f"gen{gen}{tier}"):
                return f"gen{gen}{tier}-1500.txt"
        except ValueError:
            try:
                if tiers.index(tier) and tier == (6 | 7):
                    return f"{tier}-1500.txt"
            except ValueError:
                return "Nothing found."

    def search(self) -> list[list]:
        """
        Searches the smogon stats repository and returns a list of lists.
        """
        # send the request to get the data
        res = requests.get(self.base)
        # get the text if there is any (should add a check in here)
        data = res.text
        # send each "unit" of information to a list by splitting on linebreaks
        data = data.split("\n")
        # truncate to get rid of the non-relevant prefixes and last two lines of styling
        data = data[5:-2]
        # remove the formatting
        data = self._remove_formatting(data, isMonotype=self.isMonotype)
        return data


class BaseStatsSearch(StatsSearch):
    """>tier (str): string of tier to be queried."""

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
        self._build_url()

    @property
    def tier(self) -> str:
        return self._tier.lower()

    @tier.setter
    def tier(self, value):
        self._tier = value

    def _build_url(self):
        # Rating of 1500 is defined by Smogon as their target of a normal player

        validation_object = self._create_validation_object()
        validator = Validations(validation_object)
        # check dates for valid tiers
        # since for now I am only looking up newer stats for database, it will be fine
        if validator.validate():
            if Validations.is_modern_format(validation_object):
                ending = f"gen{self.gen}{self.tier}-1500.txt"
                self.ending = ending
                self.base += ending
            else:
                ending = self._vintage_search(
                    self.year, self.month, self.gen, self.tier
                )
                # below can be deleted after validations are done
                if ending.endswith(".txt"):
                    self.ending = ending
                    self.base += ending
                # else:
                #     raise Exception('Invalid information supplied, check your parameters.')
        else:
            print("Something isn't correct.")


class MonotypeStatsSearch(StatsSearch):
    """>typing (str): string of type to be queried."""

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
        self.base += f"{year}-{month}/monotype/"
        self._build_url()
        self.isMonotype = True

    @property
    def typing(self) -> str:
        return self._typing.lower()

    @typing.setter
    def typing(self, value):
        self._typing = value

    # I could probably combine this and the other into a singular _build_url() that lives in the parent class, but I think this is simpler
    def _build_url(self):
        # Rating of 1500 is defined by Smogon as their target of a normal player

        validation_object = self._create_validation_object()
        validator = Validations(validation_object)
        print(validation_object)
        # check dates for valid tiers
        # since for now I am only looking up newer stats for database, it will be fine
        if validator.validate(isMonotype=True):
            ending = f"gen{self.gen}monotype-mono{self.typing}-1500.txt"
            self.ending = ending
            self.base += ending
        else:
            print("Something isn't correct.")


if __name__ == "__main__":
    base_search = BaseStatsSearch("2023", "06", "9", "ou")
    base_search_data = base_search.search()
    print(base_search._create_validation_object())
    print(base_search_data[3])

    mono_search = MonotypeStatsSearch("2022", "06", "8", "psychic")
    mono_search_data = mono_search.search()
    print(mono_search._create_validation_object())
    print(mono_search_data[0:5])

# --------------------------------
# Imports
# --------------------------------
import os
import sys
import time
import json
import requests
import datetime
import pandas as pd
from _utils import *

"""
TODO:

- branch for monotype
- write update functions to require no input and run from a .sh or batch file
- anything else i think of
"""

POKEDICT = pokedict()
# --------------------------------
# Global variables for default use
# --------------------------------
RATINGS = ["1630", "1695"] #["0", "1500", "1630", "1695", "1760"]

YEARS = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]

MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

GENS = ["8", "7", "6", "5", "4", "3", "2", "1"]

TIERS = [
    "ou",
    "ubers",
    "1v1",
    "pu",
    "nu",
    "lc",
    "uu",
    "ru",
    "customgame",
    "2v2doubles",
    "doubles",
    "anythinggoes",
    "almostanyability",
    "balancedhackmons",
    "battlefactory",
    "battlespotsingles",
    "battlespotdoubles",
    "battlespotspecial",
    "bssfactory",
    "budoubles",
    "busingles",
    "camomons",
    "cap",
    "challengecup",
    "challengecup1v1",
    "doublescustomgame",
    "doublesou",
    "doublesubers",
    "doublesuu",
    "hackmonscup",
    "inversebattle",
    "lcuu",
    "linked",
    "mixandmega",
    "monotype",
    "natureswap",
    "nfe",
    "ounomega",
    "randombattle",
    "randomdoublesbattle",
    "randomtriplesbattle",
    "stabmons",
    "smogontriples",
    "tiershift",
    "ultrakalosclassic",
    "vcg2018",
    "vgc2014",
    "vgc2015",
    "vgc2016",
    "vgc2017",
    "vgc2019",
    "vgc2020",
    "zu",
    "doubleslc"
]

MONOTYPES = [
    "monodark",
    "monobug",
    "monodragon",
    "monofighting",
    "monoflying",
    "monopoison",
    "monofairy",
    "monofire",
    "monowater",
    "monoelectric",
    "monograss",
    "monosteel",
    "monoground",
    "monorock",
]


# --------------------------------
# The whole script
# --------------------------------
class Contact_Smogon:
    def __init__(
        self,
        years: list,
        months: list,
        gens: list,
        tiers: list,
        ratings: list,
        mono: bool = False,
        monotype: list = [""],
        suspect: bool = False,
    ):
        self.years = years  # needs to be list of 4 digit year
        self.months = months  # needs to be list of 2 digit month, ie 03 for March
        self.ratings = ratings
        self.tiers = tiers
        self.gens = gens
        self.mono = mono
        self.monotype = monotype
        self.suspect = suspect
        self._urls = []

        self._base = r"https://www.smogon.com/stats/"
        # self._path = os.getcwd()
        # self._temp_path = ""

        self.__temp = make_temp()
        self.__urls = self.__set_urls()

    # --------------------------------
    # Url handler methods.
    # --------------------------------
    def urls(self):
        return self._urls

    def __set_urls(self):
        for y in self.years:
            for m in self.months:
                for g in self.gens:
                    for t in self.tiers:
                        for r in self.ratings:
                            gtr = "gen{g}{t}-{r}".format(g=g, t=t, r=r)
                            # nr1 = "1695"
                            # nr2 = "1825"
                            url = self._base + "{y}-{m}/{gtr}.txt".format(
                                y=y, m=m, gtr=gtr
                            )
                            self._urls.append(url)
                            # if gtr == "gen8ou-1630":
                            #     url = self._base + "{y}-{m}/gen{g}{t}-{nr1}.txt".format(
                            #         y=y, m=m, g=g, t=t, nr1=nr1
                            #     )
                            #     self._urls.append(url)
                            # elif gtr == "gen8ou-1760":
                            #     url = self._base + "{y}-{m}/gen{g}{t}-{nr2}.txt".format(
                            #         y=y, m=m, g=g, t=t, nr2=nr2
                            #     )
                            #     self._urls.append(url)
                            # else:
                            #     url = self._base + "{y}-{m}/{gtr}.txt".format(
                            #         y=y, m=m, gtr=gtr
                            #     )
                            #     self._urls.append(url)

    # --------------------------------
    # Stats retreival.
    # --------------------------------
    def find_stats(self, output_type):  # , urls):  # ,gen,tier,rating):

        if not (output_type == "json" or output_type == "csv"):
            raise ValueError("Please select either 'json' or 'csv' for output.")
        # List of all valid ratings.
        rating_list = [
            "0",
            "1500",
            "1630",
            "1760",
            "1695",
            "1825",
        ]

        for url in self._urls:

            # Do the request to get data page
            try:
                r = requests.get(url)
            except:
                continue
            page = r.text
            if not page.startswith("<html>"):

                # Parse out date and tier information from the url address.
                src = url.split("/")
                src = src[4:]
                date = src[0]

                gtr = src[1].strip(".txt")
                tier = gtr.split("-")
                tier = tier[0]

                # Create the filenames for the temp files to save.
                page_path = self.__temp + f"{'_'.join(src)}"

                # save and read it.
                with open(page_path, "w") as f:
                    f.write(page)
                    f.close()

                # Draw the rest of the owl
                fobj = open(page_path)
                data_list = formating(fobj)
                create_data_structure(data_list, date, tier, save_as=output_type)
                os.remove(page_path)
                time.sleep(3)
            else:
                pass

        clear_temp_files()
        combine_all_csv()
        return

def update():
    today = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m")
    date = today.split('-')
    year = date[0]
    month = date[1]
    cs = Contact_Smogon([year], [month], GENS, TIERS, RATINGS)
    cs.urls()
    cs.find_stats("csv")

if __name__ == "__main__":

    # cs = Contact_Smogon(["2021"], ["08"], ["8"], ["ubers"], ["1630"])
    cs = Contact_Smogon(["2021"], ["03", "04"], GENS, TIERS, ["1630", "1695"])
    cs.urls()
    cs.find_stats("csv")

    # update()

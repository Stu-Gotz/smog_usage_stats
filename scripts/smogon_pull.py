# --------------------------------
# Imports
# --------------------------------
import os
import re
import sys
import time
import uuid
import json
import shutil
import requests
import pandas as pd

"""
trees = ['chaos','leads','mega','metagame','monotype','moveset']

suspect = set to bool; true="suspecttest", false=none
monotype toggle too
"""

# --------------------------------
# Global variables for default use
# --------------------------------
RATINGS = ["0", "1500", "1630", "1760"]

YEARS = ["2020", "2019", "2018", "2017", "2016", "2015", "2014"]

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
    "monoice",
    "mononormal",
    "monoghost",
    "monodark",
    "monopsychic",
]


# --------------------------------
# The whole script
# --------------------------------
class Contact_Smogon:
    def __init__(
        self,
        years=["2020"],
        months=["02"],
        gens=["8"],
        tiers=["ou"],
        ratings=["1630"],
        mono=False,
        monotype="monoice",
    ):
        self.years = years  # needs to be list of 4 digit year
        self.months = months  # needs to be list of 2 digit month, ie 03 for March
        self.ratings = ratings
        self.tiers = tiers
        self.gens = gens
        self.mono = mono
        self.monotype = monotype
        self._urls = []

        self._base = r"https://www.smogon.com/stats/"
        self._path = os.getcwd()
        self._temp_path = ""

        self.__temp = self._make_temp()
        self.__urls = self.__set_urls()

    # --------------------------------
    # Temp folder management methods
    # --------------------------------
    def _make_temp(self):
        if sys.platform.lower().startswith("win"):
            self._temp_path = os.path.join(self._path + r"\data\temp\\")
        else:
            self._temp_path = os.path.join(self._path + "/data/temp/")
        try:
            os.mkdir(self._temp_path)
            print("Created temporary folder at {}.".format(self._temp_path))
        except FileExistsError:
            print("Temp folder already exists at {}.".format(self._temp_path))
        return

    def clear_temp_files(self):
        # temp_path = os.fsencode(_temp_folder)
        shutil.rmtree(self._temp_path)
        print("Temporary files have been removed from {}.".format(self._temp_path))
        return

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
                            nr1 = "1695"
                            nr2 = "1825"
                            if gtr == "gen8ou-1630":
                                url = self._base + "{y}-{m}/gen{g}{t}-{nr1}.txt".format(
                                    y=y, m=m, g=g, t=t, nr1=nr1
                                )
                                self._urls.append(url)
                            elif gtr == "gen8ou-1760":
                                url = self._base + "{y}-{m}/gen{g}{t}-{nr2}.txt".format(
                                    y=y, m=m, g=g, t=t, nr2=nr2
                                )
                                self._urls.append(url)
                            else:
                                url = self._base + "{y}-{m}/{gtr}.txt".format(
                                    y=y, m=m, gtr=gtr
                                )
                                self._urls.append(url)

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
        for u in self._urls:
            for r in rating_list:
                if r not in rating_list:  # throw error if invalid rating.
                    raise ValueError(
                        "Invalid rating input. Rating value must be 1 of 0, 1500, 1630, 1695, 1760, or 1825."
                    )

        for url in self._urls:

            # Do the request to get data page
            r = requests.get(url)
            page = r.text

            # Parse out date and tier information from the url address.
            src = url.split("/")
            src = src[4:]

            date = src[0]

            gtr = src[1].split(".")
            gtr = gtr[0]

            # Create the filenames for the temp files to save.
            page_path = self._temp_path + r"{}_{}".format(src[0], src[1])

            # save and read it.
            with open(page_path, "w") as f:
                f.write(page)
                f.close()

            # Draw the rest of the owl
            fobj = open(page_path)
            data_list = self.__remove_formatting(fobj)
            self.__create_data_structure(data_list, date, gtr, save_as=output_type)
            time.sleep(5)

        self.clear_temp_files()
        return

    # --------------------------------
    # Organise the clean data to either json or csv output
    # --------------------------------
    def __create_data_structure(self, data_list, date, gtr, save_as="csv"):

        # Keys to be used in the dictionary creation below
        keys = [
            "rank",
            "pokemon",
            "usage_pct",
            "raw_usage",
            "raw_pct",
            "real",
            "real_pct",
        ]

        # List to hold dicts to be turned into a dataframe/csv or json
        dict_list = []

        # Create the list of dictionaries
        for data in data_list:
            data_split = data.split(",")
            data_dict = dict(zip(keys, data_split))
            dict_list.append(data_dict)

        # Send to csv or json, based on what user prefers. Default is csv because its generally easier for python
        if save_as == "csv":
            csv_path = os.path.join(self._path, "data/csv/")
            df = pd.DataFrame(dict_list)
            if not os.path.exists(csv_path):
                os.mkdir(csv_path)

            df.to_csv(
                os.path.join(
                    self._path,
                    "data/csv/{d}_{gtr}.csv".format(d=date, gtr=gtr),
                ),
                index=False,
            )
        elif save_as == "json":
            json_path = os.path.join(self._path, "data/json/")

            if not os.path.isdir(json_path):
                os.mkdir(json_path)

            json_out = dict(
                zip(["pos" + str(x) for x in range(len(dict_list))], dict_list)
            )
            with open(
                os.path.join(
                    self._path, "data/json/{d}_{gtr}.json".format(d=date, gtr=gtr)
                ),
                "w",
            ) as f:
                json.dump(json_out, f)

    # --------------------------------
    # Take the formatted text page to essentially a list of rows
    # --------------------------------
    def __remove_formatting(self, page):

        outlist = []

        # read lines of file with .readlines() and truncate the first 6 lines of
        # formatting
        listOfLines = page.readlines()
        listOfLines = listOfLines[5:]

        # Remove the formatting that clogs up the pipes.
        for line in listOfLines:
            line = line.replace("|", ",")
            line = line.replace(" ", "")
            line = line.replace("%", "")
            if line.startswith(","):
                line = line[1:-2]
                outlist.append(line)

        return outlist  # return the list


if __name__ == "__main__":

    cs = Contact_Smogon()
    cs.urls()
    cs.find_stats("csv")
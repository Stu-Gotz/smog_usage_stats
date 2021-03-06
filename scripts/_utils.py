import os
import sys
import json
import time
import shutil
from datetime import datetime
import pandas as pd

__BASE = r"https://www.smogon.com/stats/"
__PATH = os.getcwd()


def pokedict():
    """Creates a dictionary of pokedex data."""
    j = open(str(os.path.join(__PATH, "data/reference/pokedex.json")))
    _pokedict = json.load(j)
    return _pokedict

pokedict()

def make_temp():
    """Create temporary folders to store temporary data."""
    if sys.platform.lower().startswith("win"):
        _TEMP_PATH = os.path.join(__PATH + r"\data\\temp\\")
    else:
        _TEMP_PATH = os.path.join(__PATH + "/data/temp/")
    try:
        os.mkdir(_TEMP_PATH)
        print(f"Created temporary folder at {_TEMP_PATH}.")
    except FileExistsError:
        print(f"Temp folder already exists at {_TEMP_PATH}.")
    return _TEMP_PATH


TEMP_PATH = make_temp()


def clear_temp_files():
    """Removes temporary files and folder."""
    shutil.rmtree(TEMP_PATH)
    message = f"Temporary files have been removed from {TEMP_PATH}."
    return {"message": message}


def find_dex(row):
    '''
    Associates each pokemon with it's pokedex number.
    
        Args:
            row (list): A row of data from the usage stats.
        Returns:
            dex (list): An updated list from `row` with the pokedex number.
    '''
    pokemon_name = row[1].lower().replace("-totem", "")
    pokedex = pokedict()
    try:
        dex = pokedex["data"][pokemon_name]["pokedex_number"]
    except KeyError:
        dex = -1
    return dex


# --------------------------------
# Removing formatting from recieved data
# --------------------------------
def formating(page):
    '''
    Formats the page from the webpage into an list of lists containing the stats.

        Args:
            page (object):
    '''
    outlist = []

    # read lines of file with .readlines() and truncate the first 6 lines of
    # formatting
    listOfLines = page.readlines()
    listOfLines = listOfLines[5:]

    # Remove the formatting that clogs up the pipes.
    for line in listOfLines:
        line = line.replace("|", ",").replace(" ", "").replace("%", "")
        if line.startswith(","):
            line = line[1:-2]
            outlist.append(line)
    return outlist

#---------------------------------
# Creates the dataframe and saves to csv
#---------------------------------
def create_data_structure(data_list, date, tier, save_as="csv"):

    # Keys to be used in the dictionary creation below
    keys = [
        "rank",
        "pokemon",
        "usage_pct",
        "raw_usage",
        "raw_pct",
        "real",
        "real_pct",
        "dex",
        "date",
        "tier",
    ]

    # List to hold dicts to be turned into a dataframe/csv or json
    dict_list = []

    # Create the list of dictionaries
    for data in data_list:
        data_split = data.split(",")
        dex = find_dex(data_split)
        data_split.extend([dex, date, tier])
        data_dict = dict(zip(keys, data_split))
        for i in data_dict.keys():
            if type(data_dict[i]) is str:
                data_dict[i] = data_dict[i].lower()
        dict_list.append(data_dict)

    # Send to csv or json, based on what user prefers. Default is csv because its generally easier for python
    pokemon_df = pd.DataFrame(dict_list)
    if save_as == "csv":
        csv_path = os.path.join(__PATH, "data/csv/")
        if not os.path.exists(csv_path):
            os.mkdir(csv_path)

        pokemon_df.to_csv(
            os.path.join(
                __PATH,
                f"data/csv/{date}_{tier}.csv",
            ),
            index=False,
        )
    elif save_as == "json":
        json_path = os.path.join(__PATH, "data/json/")

        if not os.path.isdir(json_path):
            os.mkdir(json_path)

        json_out = dict(
            zip(["rank" + str(x + 1) for x in range(len(dict_list))], dict_list)
        )
        with open(
            os.path.join(__PATH, f"data/json/{date}_{tier}.json"),
            "w",
        ) as f:
            json.dump(json_out, f)
    return f"{date} {tier} file created as a {save_as}."

#---------------------------------
# Merges all separate csvs to a single csv to feed to the db
#---------------------------------
def combine_all_csv():

    csv_path = os.path.join(__PATH, "data/csv/")
    
    dir_list = os.listdir(csv_path)
    output = os.path.join(__PATH, "data/statsmaster.csv")
    fout = open(output, "a")
    for f in range(len(dir_list)):

        if f == 0:
            continue
            x = open(csv_path + dir_list[f])
            for line in x:
                fout.write(line)
            x.close()
        else:
            x = open(csv_path + dir_list[f])
            next(x, None)
            for line in x:
                fout.write(line)
            x.close()
    fout.close()
    return

#---------------------------------
# Append new data to master csv file for autorun.
#---------------------------------
def update_csv():

    date = datetime.strftime(datetime.datetime.today(), "%Y-%m")
    csv_path = os.path.join(__PATH, "data/")
    csv_dir = os.path.join(__PATH, "data/csv")

    csv_dir_list = os.listdir(csv_dir)

    with open(os.path.join(csv_path, 'statsmaster.csv'), 'a') as f:
        for csv in csv_dir_list:
            if (date in csv) and (datetime.strftime(time.ctime(os.path.getctime(csv)), "%Y-%m") is not date):
                next(csv, None)
                for line in csv:
                    f.write(line)
        
        f.close()
        return
import os
import sys
import json
import shutil
import pandas as pd

__BASE = r"https://www.smogon.com/stats/"
__PATH = os.getcwd()

# --------------------------------
# Get a dictionary of the Pokedex
# --------------------------------
def pokedict():
    _pokedict = {"data": {}}
    with open(
        "/home/alan/dev/smog_usage_stats/data/reference/pokedex.json"
    ) as json_file:
        pokedex = json.load(json_file)
        for entry in pokedex:
            name = entry["name"]
            tdict = {str(name): entry}
            # print(tdict)
            _pokedict["data"].update(tdict)
    return _pokedict


# --------------------------------
# Temp folder management methods
# --------------------------------
TEMP_PATH = ""


class PathTools:
    def make_temp():
        if sys.platform.lower().startswith("win"):
            TEMP_PATH = os.path.join(__PATH + r"\data\temp\\")
        else:
            TEMP_PATH = os.path.join(__PATH + "/data/temp/")
        try:
            os.mkdir(TEMP_PATH)
            print(f"Created temporary folder at {TEMP_PATH}.")
        except FileExistsError:
            print(f"Temp folder already exists at {TEMP_PATH}.")
        return TEMP_PATH

    def clear_temp_files(self):
        shutil.rmtree(TEMP_PATH)
        message = f"Temporary files have been removed from {TEMP_PATH}."
        return {"message": message}


# --------------------------------
# Removing formatting from recieved data
# --------------------------------
def formating(page):

    outlist = []

    # read lines of file with .readlines() and truncate the first 6 lines of
    # formatting
    listOfLines = page.readlines()
    listOfLines = listOfLines[5:]

    # Remove the formatting that clogs up the pipes.
    for line in listOfLines:
        line = line.replace("|", ",").replace(" ", "").replace("%", "")
        line_as_list = line.split(",")
        for word in line_as_list:
            try:
                (int(word) | float(word))

            except:
                word = word.lower()
                # try:
                pokeobj = pokedex.Pokedex()
                pokemon = pokeobj.get_pokemon_by_name(word)
                print(pokemon)
                # except:
                #     print(word)

        if line.startswith(","):
            line = line[1:-2]
            outlist.append(line)
    return outlist


def create_data_structure(data_list, date, gtr, save_as="csv"):

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
                f"data/csv/{d}_{gtr}.csv",
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
            os.path.join(__PATH, f"data/json/{d}_{gtr}.json"),
            "w",
        ) as f:
            json.dump(json_out, f)

    return pokemon_df


# def combine_all_csv():

#     csv_path = "/home/alan/dev/smog_usage_stats/data/csv/"

#     dir_list = os.listdir(csv_path)
#     output = "/home/alan/dev/smog_usage_stats/data/statsmaster.csv"
#     fout = open(output, "a")
#     for f in range(len(dir_list)):

#         if f == 0:
#             x = open(csv_path + dir_list[f])
#             for line in x:
#                 fout.write(line)
#             x.close()
#         else:
#             x = open(csv_path + dir_list[f])
#             next(x, None)
#             for line in x:
#                 fout.write(line)
#             x.close()
#     fout.close()
#     return "deleted"


# combine_all_csv()
print(os.getcwd())
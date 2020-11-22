import pandas as pd
import os
import zipfile
import json
from pokedex_copy import pokedex

# print(pokedex)


import pandas as pd
import os

PATH = os.getcwd() + "/data/reference"
df = pd.read_csv(PATH + "/pokedex.csv", header=0)
df.to_json(PATH + "/pokedex.json", orient="records")
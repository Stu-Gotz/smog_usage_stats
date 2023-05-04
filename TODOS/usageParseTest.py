import re


def splitList(inlist, sep):
    s = []
    for el in inlist:
        if el == sep:
            yield s
            s = []
        s.append(el)
    yield s


# def dashrepl(matchobj):
#     pattern = re.match()
#      if matchobj.group(0) == '': return ' '
#      else: return '-'

# with open(r"./scripts/statsparsetest.txt") as f:
#     # print(f.read())

#     pattern = "'\#{2,}'"
#     fList = list()
#     listOfLines = f.readlines()
#     print(len(listOfLines))

#     for l in listOfLines:
#         l = l.replace("\n", "")
#         l = l.replace("|", ",")
#         l = l.replace("  ", "#")
#         l = l.replace("\t", "")
#         l = l.replace(" , ", "")
#         l = l.replace(", ", "")
#         l = l.replace(" ,", "")
#         l = l.replace("%", "")
#         l = l.replace(" +----------------------------------------+ ", ";")
#         # l = re.sub(l, )

#         print(l)

#         # if l.startswith(","):
#         #     l = l[1:]
#         #     print(l)
#         fList.append(l)

# print(fList)

# newlist = []
# for f in fList:
#     x = re.sub(r"\#{2,}", "", f)
#     x = re.sub(r"#", " ", x)
#     newlist.append(x)

# # finalList = list(splitList(newlist[1:], ";"))
# print(finalList)


# def list_to_object(inputList):

#     pokemonObject = {}
#     pokemonObject["name"] = inputList[0][0]
#     print(pokemonObject["name"])

#     return pokemonObject


# list_to_object(finalList)

# [
#     ["Vullaby"],
#     [";", "Raw count: 28689", "Avg. weight: 0.36221242656", "Viability Ceiling: 88"],
#     [";", "Abilities", "Weak Armor 75.216", "Overcoat 24.436", "Big Pecks 0.348"],
#     [
#         ";",
#         "Items",
#         "Berry Juice 65.728",
#         "Eviolite 24.563",
#         "Choice Scarf 8.870",
#         "Other 0.839",
#     ],
#     [
#         ";",
#         "Spreads",
#         "Jolly:0/236/76/0/0/196 18.373",
#         "Adamant:0/236/76/0/0/196 16.124",
#         "Modest:0/0/76/236/0/196 7.743",
#         "Modest:116/0/0/236/0/116 6.142",
#         "Modest:0/0/0/236/236/36 2.579",
#         "Adamant:0/236/0/0/76/196 2.510",
#         "Other 46.528",
#     ],
#     [
#         ";",
#         "Moves",
#         "Brave Bird 72.496",
#         "Knock Off 72.392",
#         "U-turn 60.451",
#         "Defog 51.866",
#         "Heat Wave 45.996",
#         "Air Slash 26.383",
#         "Nasty Plot 25.643",
#         "Dark Pulse 23.374",
#         "Roost 11.661",
#         "Other 9.739",
#     ],
#     [
#         ";",
#         "Teammates",
#         "Timburr +4.667",
#         "Mareanie +4.620",
#         "Ferroseed +4.131",
#         "Trapinch +2.984",
#         "Diglett +2.425",
#         "Mudbray +2.223",
#         "Oddish +1.762",
#         "Foongus +1.120",
#         "Corphish +1.040",
#         "Budew +0.804",
#         "Ponyta-Galar +0.552",
#         "Onix +0.513",
#     ],
#     [
#         ";",
#         "Checks and Counters",
#         "Onix 82.059 (87.74±1.42)",
#         "(14.5 KOed / 73.3 switched out)",
#         "Spritzee 67.144 (75.71±2.14)",
#         "(23.1 KOed / 52.6 switched out)",
#         "Shellder 58.729 (80.57±5.46)",
#         "(47.5 KOed / 33.1 switched out)",
#         "Pawniard 56.671 (65.51±2.21)",
#         "(19.8 KOed / 45.7 switched out)",
#         "Corphish 51.827 (72.71±5.22)",
#         "(45.8 KOed / 26.9 switched out)",
#         "Abra 50.735 (64.98±3.56)",
#         "(37.7 KOed / 27.2 switched out)",
#     ],
#     [";"],
# ]

import pandas as pd
import os
import json

df = pd.read_csv(r"C:\dev\python\smog_usage_stats\TODOS\Pokedex_Ver_SV2.csv", header=0)
df.fillna("", inplace=True)
recs = df.to_dict(orient="records")

dex = []

for rec in recs:

    if 'alolan' in rec['name']:
        newname = rec['name'].strip('alolan ')
        newname += '-alola'
        rec['name'] = newname
    elif 'galarian' in rec['name']:
        newname = rec['name'].strip('galarian ')
        newname += '-galar'
        rec['name'] = newname
    elif 'hisuian' in rec['name']:
        newname = rec['name'].strip('hisuian ')
        newname += '-hisui'
        rec['name'] = newname
    elif 'paldean' in rec['name']:
        newname = rec['name'].strip('paldean ')
        newname += '-paldea'
        rec['name'] = newname

    newdict = {}
    newdict[rec["name"]] = rec
    dex.append(newdict)

with open("testdex.json", "w") as f:
    json.dump(dex, f)
    f.close()
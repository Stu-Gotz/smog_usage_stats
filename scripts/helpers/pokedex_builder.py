# GOAL: Build Pokedex from Pokeapi
# Step 1: get list of all pokemon names
# Step 2: Compile data together in large object according to existing pokemon.json file
# Step 3: Make calculator for weakness types (dict{type:{matchups: {super: [list, of, types]}, {weakness: [list, of, types]}})
#       - multiply for each type1/type2 eg: psychic/flying gets psychic check then multiply (2x SE, .5x weak), then flying
# Step 4: add link in pokedex json
# Step 5: overwrite pokedex.json


# example
# {
# "data": {
#     "bulbasaur": {
#         "pokedex_number": 1,
#         "name": "bulbasaur",
#         "type_1": "grass",
#         "type_2": "poison",
#         "ability_1": "overgrow",
#         "ability_2": null,
#         "ability_hidden": "chlorophyll",
#         "total_points": 318,
#         "hp": 45,
#         "attack": 49,
#         "defense": 49,
#         "sp_attack": 65,
#         "sp_defense": 65,
#         "speed": 45,
#         "against_normal": 1.0,
#         "against_fire": 2.0,
#         "against_water": 0.5,
#         "against_electric": 0.5,
#         "against_grass": 0.25,
#         "against_ice": 2.0,
#         "against_fight": 0.5,
#         "against_poison": 1.0,
#         "against_ground": 1.0,
#         "against_flying": 2.0,
#         "against_psychic": 2.0,
#         "against_bug": 1.0,
#         "against_rock": 1.0,
#         "against_ghost": 1.0,
#         "against_dragon": 1.0,
#         "against_dark": 1.0,
#         "against_steel": 1.0,
#         "against_fairy": 0.5
#     },
import json
import os
import requests
from pokelist import PokeList
from typechart import TypeChart

def build_pokedex():
  template= {
      "pokedex_number": 0,
      "name": "",
      "type_1": "",
      "type_2": "",
      "ability_1": "",
      "ability_2": "",
      "ability_hidden": "",
      "total_points": 0,
      "hp": 0,
      "attack": 0,
      "defense": 0,
      "sp_attack": 0,
      "sp_defense": 0,
      "speed": 0,
      "against_normal": 1.0,
      "against_fire": 1.0,
      "against_water": 1.0,
      "against_electric": 1.0,
      "against_grass": 1.0,
      "against_ice": 1.0,
      "against_fight": 1.0,
      "against_poison": 1.0,
      "against_ground": 1.0,
      "against_flying": 1.0,
      "against_psychic": 1.0,
      "against_bug": 1.0,
      "against_rock": 1.0,
      "against_ghost": 1.0,
      "against_dragon": 1.0,
      "against_dark": 1.0,
      "against_steel": 1.0,
      "against_fairy": 1.0
      }
  
  output = {"data":{}}

  list_of_pokemon = PokeList().pokelist()
  type_chart = TypeChart.typechart()

  # pokeapi = r"https://pokeapi.co/api/v2/pokemon/"


  for pokemon in list_of_pokemon[0:3]:
    # r = requests.get(''.join(pokeapi, pokemon))

    # data = r.json()

    stats = data["stats"]
    stats_dict = {
      "hp":stats[0]["base_stat"],
      "attack": stats[1]["base_stat"],
      "defense": stats[2]["base_stat"],
      "sp_attack": stats[3]["base_stat"],
      "sp_defense": stats[4]["base_stat"],
      "speed":stats[5]["base_stat"],
      "total_poitns": stats_dict["hp"]+stats_dict["attack"]+stats_dict["defense"]
                      +stats_dict["sp_attack"]+stats_dict["sp_defense"]
                      +stats_dict["speed"]
    }
    target = output["data"]
    target[pokemon] =  {
      "pokedex_number": data["id"],
      "name": pokemon,
      "against_normal": 1.0,
      "against_fire": 1.0,
      "against_water": 1.0,
      "against_electric": 1.0,
      "against_grass": 1.0,
      "against_ice": 1.0,
      "against_fight": 1.0,
      "against_poison": 1.0,
      "against_ground": 1.0,
      "against_flying": 1.0,
      "against_psychic": 1.0,
      "against_bug": 1.0,
      "against_rock": 1.0,
      "against_ghost": 1.0,
      "against_dragon": 1.0,
      "against_dark": 1.0,
      "against_steel": 1.0,
      "against_fairy": 1.0
    }

    target.update(stats_dict)

    print(target)
    print(output)

dummy = {"data":{}}
r = requests.get(r"https://pokeapi.co/api/v2/pokemon/bulbasaur")
d = r.json()

target = dummy
new_target = target["data"]["bulbasaur"] = {}
print(target)
print(new_target)
new_target["name"] = "bulbsaur"
new_target["pokedex_number"] = 1
print(new_target)
print(target)

build_pokedex()
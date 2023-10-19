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
#     },
import json
import os
import requests
from pokelist import PokeList
from typechart import TypeChart




class PokedexEntry():
  def __init__(self):
    self.template= {
      "dex": 0,
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
      }
  
  @staticmethod
  def set_template(self, field, value):
    self.template[field] = value
    
  
list_of_pokemon = PokeList().pokelist()
type_chart = TypeChart().typechart()

pokeapi = r"https://pokeapi.co/api/v2/pokemon/"

output = {"data":{}}

for pokemon in list_of_pokemon[0:3]:
  r = requests.get(''.join([pokeapi, pokemon]))

  data = r.json()

  
  stats = data["stats"]
  entry = PokedexEntry().template()
  entry['']
  entry['dex'] = data['id']
  entry['name'] = data['species']
  entry['type_1'] = data['types'][0]['type']['name']
  entry['type_2'] = data['types'][1]['type']['name'] or ""
  entry['ability_1'] = data['abilities'][0]['ability']['name']

  print(entry)

# dummy = {"data":{}}
# r = requests.get(r"https://pokeapi.co/api/v2/pokemon/bulbasaur")
# d = r.json()

# target = dummy
# new_target = target["data"]["bulbasaur"] = {}
# print(target)
# print(new_target)
# new_target["name"] = "bulbsaur"
# new_target["pokedex_number"] = 1
# print(new_target)
# print(target)

# template()
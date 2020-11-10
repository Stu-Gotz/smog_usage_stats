import smogon_pull

import pandas as pd
import numpy as np

from bokeh.io import show, curdoc
from bokeh.plotting import figure

from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource, Panel

path = r'C:\Dev\usage_data_0.0.1\data\2014_11_lc_1760.csv'
stats_in = pd.read_csv(path, headers=0,index_col=0)

src=smogon_pull.make_dataset(initial_mons,
                 range_start=range_select.value[0])

def make_dataset():
    pass
class Make_Plot(src):
    
    def __init__(self):
        pass




# {'tier': 'gen8lc', 'pokemon': 'Vullaby', 'rank': '1', 'usage': '61.68243%',
#  'raw': '23254', 'abilities': {'Weak Armor': '81.312%', 'Overcoat': '18.384%',
# 'Big Pecks': '0.304%'}, 'items': {'Berry Juice': '58.876%', 'Eviolite': '32.187%',
# 'Choice Scarf': '8.568%', 'Other': '0.369%'}, 'spreads': {'Adamant':
# {'0/236/76/0/0/196': '18.854%'}, 'Jolly': {'0/236/76/0/0/196': '11.029%'},
# 'Modest': {'0/0/76/236/0/196': '8.405%', '116/0/0/236/0/116': '7.802%',
# '116/0/0/240/0/116': '5.885%', '0/0/0/236/236/36': '3.143%'}, 'Other': '44.882%'},
# 'moves': {'Knock Off': '61.183%', 'Brave Bird': '60.107%', 'Heat Wave': '50.549%',
# 'U-turn': '49.941%', 'Defog': '42.427%', 'Air Slash': '39.095%',
# 'Nasty Plot': '37.983%', 'Dark Pulse': '35.873%', 'Endure': '9.070%', 'Other': '13.771%'},
# 'teammates': {'Ferroseed': '+4.373%', 'Diglett': '+2.537%', 'Shellos': '+2.496%',
# 'Cutiefly': '+2.402%', 'Corphish': '+1.958%', 'Zigzagoon': '+1.731%',
# 'Koffing': '+1.435%', 'Mudbray': '+1.369%', 'Mareanie': '+0.934%',
# 'Vulpix-Alola': '+0.859%', 'Machop': '+0.842%', 'Shellder': '+0.734%'},
# 'checks': {'Onix': {'ko': '20.9%', 'switched': '62.6%'}, 'Dwebble': {'ko': '62.4%',
# 'switched': '21.5%'}, 'Spritzee': {'ko': '30.2%', 'switched': '40.6%'},
# 'Shellder': {'ko': '49.9%', 'switched': '24.5%'}, 'Cutiefly': {'ko': '34.1%',
# 'switched': '28.2%'}, 'Zigzagoon': {'ko': '56.8%', 'switched': '17.6%'},
# 'Shellos': {'ko': '11.9%', 'switched': '53.1%'}, 'Corphish': {'ko': '47.6%', 'switched': '19.0%'}}}
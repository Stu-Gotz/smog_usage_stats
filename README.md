# smog_usage_stats

A Python wrapper for interacting with Smogon's Pokemon Showdown usage stats data [found here](https://smogon.com/stats) and making it accessible in usable data structures.

## Quick Rundown

### Installing:

`pip install smog-usage-stats`

If your system uses `pip3` instead of `pip`, use that.

### How it all works

`BaseStatsSearch` -> Retrieves metagame usage statistics for non-Monotype metagames.

> `import smog_usage_stats.UsageStatsLookup as smogU`
>
> `baseSearch = smogU.BaseStatsSearch(2022, '06', 8, 'ou')`
>
> `results = baseSearch.search()`
>
> `print(results[0:5]) #truncated for brevity`
>
> [['rank', 'pokemon', 'usage_pct', 'raw_usage', 'raw_pct', 'real', 'real_pct', 'date', 'tier'], ['1', 'landorus-therian', '36.09686', '1001664', '34.149', '864772', '37.018', '2022-06', 'gen8ou'], ['2', 'ferrothorn', '22.27247', '641619', '21.874', '558654', '23.914', '2022-06', 'gen8ou'], ['3', 'dragapult', '18.41922', '532433', '18.152', '404433', '17.313', '2022-06', 'gen8ou'], ['4', 'heatran', '17.30305', '484022', '16.501', '405868', '17.374', '2022-06', 'gen8ou']]

`MonotypeStatsSearch` -> searches the monotype usage statistics

> `import smog_usage_stats.UsageStatsLookup as smogU`
>
> `monoSearch = smogU.MonotypeStatsSearch(2022, '06', 8, 'psychic')`
>
> `results = monoSearch.search()`
>
> `print(results[0:5]) #truncated for brevity`
>
> [['rank', 'pokemon', 'usage_pct', 'raw_usage', 'raw_pct', 'real', 'real_pct', 'date', 'tier'], ['1', 'tapulele', '60.25678', '8747', '56.924', '6738', '57.948', '2022-06', 'monopsychic'], ['2', 'victini', '52.14959', '7783', '50.651', '5705', '49.064', '2022-06', 'monopsychic'], ['3', 'slowbro', '45.34912', '6538', '42.548', '5106', '43.913', '2022-06', 'monopsychic'], ['4', 'mew', '35.13163', '5353', '34.837', '4247', '36.525', '2022-06', 'monopsychic']]

`BaseChaosSearch` -> searches the "Chaos" data contained within a certain month's stats
data

> `import smog_usage_stats.IndividualLookup as smogI`
>
> `baseChaos = smogI.BaseChaosSearch(year="2022", month="07", gen=8, tier="uu", name="SKARMORY")`
>
> `results = baseChaos.search()`
>
> {'Moves': {'': 41.8139391939, 'drillpeck': 375.2124391148, 'steelwing':
> 88.1257211624, 'rest': 8.5, 'autotomize': 33.465277165, 'steelbeam': 19.5408454477,
> 'sandtomb': 5.6841618934, 'xscissor': 37.8061940503, 'facade': 4.0263726246,
> 'attract': 0.2582478962, 'substitute': 64.9610651538, 'detect': 8.9170089777,
> 'tailwind': 208.4057975296, 'payback': 7.0, 'aircutter': 6.5070926138, 'aerialace':
> 11.8265479941, 'swordsdance': 178.0771715149, 'sleeptalk': 4.5, 'metalsound':
> 6.6025485193, 'airslash': 120.7352163352, 'toxic': 1946.992820672, 'swagger': 0.5,
> 'confide': 46.0, 'assurance': 0.5, ...}, 'Checks and Counters': ... (truncated) }

`MonotypeChaosSearch` -> searches the monotype chaos data contained within a certain
month's stats data

> `import smog_usage_stats.IndividualLookup as smogI`
>
> `monoChaos = smogI.MonotypeChaosSearch(year=2022, month="11", gen=9, typing="fairy", name="Gardevoir")`
>
> `result = monoChaos.search()`
>
> {'Moves': {'trick': 3.5, 'healingwish': 8.0, 'metronome': 7.0, 'futuresight': 7.0, 'mysticalfire': 4.0, 'calmmind': 15.5, 'psychic': 14.0, 'thunderbolt': 1.0, 'focusblast': 3.5, 'psyshock': 2.0, 'aurasphere': 2.5, 'nightshade': 1.0, 'moonblast': 16.0, 'willowisp': 0.5, 'shadowsneak': 1.0, 'energyball': 0.5, 'dazzlinggleam': 5.0}, 'Checks and Counters': {}, 'Abilities': {'synchronize': 3.5, 'trace': 19.5}, 'Teammates': {'Wigglytuff': 6.090649183, 'Grimmsnarl': 9.6031403892, 'Hatterene': 13.3468947861, 'Sylveon': 12.4625263815, 'Klefki': 10.8593859923, 'Dedenne': 10.3468947861, 'Azumarill': 11.6031403892, 'Florges': 1.0, 'Mimikyu': 17.5781579769}, 'usage': 0.5768955, 'Items': {'leftovers': 2.5, 'lifeorb': 1.0, 'choicescarf': 7.5, 'rockyhelmet': 4.0, 'wiseglasses': 1.0, 'adrenalineorb': 7.0}, 'Raw count': 46, 'Spreads': {'Timid:0/0/4/252/0/252': 4.0, 'Naughty:72/40/48/252/52/44': 7.0, 'Hasty:0/4/0/252/0/252': 1.0, 'Hardy:0/0/0/252/4/252': 4.0, 'Timid:4/0/0/252/0/252': 1.0, 'Timid:0/0/0/252/4/252': 6.0}, 'Happiness': {'255': 23.0}, 'Viability Ceiling': [0, 0, 0, 0]}

`IndividualStatsSearch` -> Retrieves usage stats from a single individual pokemon
from a certain month's stats data

> `import smog_usage_stats.IndividualLookup as smogI`
>
> `individualStats = smogI.IndividualStatsSearch(2022, "11", "8", "ou", "scIzor")`
>
> `results = individualStats.search()`
>
> {'rank': '44', 'pokemon': 'scizor', 'usage_pct': '3.50114', 'raw_usage': '67725', 'raw_pct': '3.565', 'real': '51565', 'real_pct': '3.440', 'date': '2022-11', 'tier': 'gen8ou'}

## Contributing:

If you find a bug, please [make an issue](https://github.com/Stu-Gotz/smog_usage_stats/issues).

If you would like to contribute, feel free to create a fork and submit a pull request.

## License

MIT License

Copyright (c) 2023 Stu-Gotz

# smog_usage_stats

A Python wrapper for interacting with Smogon's Pokemon Showdown usage stats data [found here](https://smogon.com/stats) and making it accessible in usable data structures.

## Quick Rundown

### Installing:

`pip install smog-usage-stats` or `uv add smog-usage-stats`.

If your system uses `pip3` instead of `pip`, use that.


### How it all works

Every lookup starts with a `Metagame`, which describes *which* stats you want: the year, month, generation, and either a `tier` or a `mono_type`. It's then passed to one of the lookup functions.

Inputs are flexible, so `month=6`, `month="6"` and `month="06"` all work, and tiers, types and names are case-insensitive. Invalid combinations (a month before Smogon's stats begin, a generation that didn't exist yet, a made-up type) raise an `InvalidFormatError` straight away, before anything is downloaded.

#### `usage_stats` → usage statistics for a whole metagame

```python
from smog_usage_stats import Metagame, usage_stats

results = usage_stats(Metagame(2022, 6, 8, tier="ou"))

print(results[:4])  # truncated for brevity
```

```
[Usage(rank=1, pokemon='landorus-therian', usage_pct=36.09686, raw_usage=1001664, raw_pct=34.149, real=864772, real_pct=37.018, date='2022-06', tier='gen8ou'),
 Usage(rank=2, pokemon='ferrothorn', usage_pct=22.27247, raw_usage=641619, raw_pct=21.874, real=558654, real_pct=23.914, date='2022-06', tier='gen8ou'),
 Usage(rank=3, pokemon='dragapult', usage_pct=18.41922, raw_usage=532433, raw_pct=18.152, real=404433, real_pct=17.313, date='2022-06', tier='gen8ou'),
 Usage(rank=4, pokemon='heatran', usage_pct=17.30305, raw_usage=484022, raw_pct=16.501, real=405868, real_pct=17.374, date='2022-06', tier='gen8ou')]
```

Each row is a `Usage` object with real numbers, so you can sort, filter and compare directly:

```python
results[0].pokemon      # 'landorus-therian'
results[0].usage_pct    # 36.09686
results[0].as_dict()    # {'rank': 1, 'pokemon': 'landorus-therian', ...}
```

#### Monotype → pass `mono_type` instead of `tier`

```python
from smog_usage_stats import Metagame, usage_stats

results = usage_stats(Metagame(2022, 6, 8, mono_type="psychic"))

print(results[:4])  # truncated for brevity
```

```
[Usage(rank=1, pokemon='tapulele', usage_pct=60.25678, raw_usage=8747, raw_pct=56.924, real=6738, real_pct=57.948, date='2022-06', tier='monopsychic'),
 Usage(rank=2, pokemon='victini', usage_pct=52.14959, raw_usage=7783, raw_pct=50.651, real=5705, real_pct=49.064, date='2022-06', tier='monopsychic'),
 Usage(rank=3, pokemon='slowbro', usage_pct=45.34912, raw_usage=6538, raw_pct=42.548, real=5106, real_pct=43.913, date='2022-06', tier='monopsychic'),
 Usage(rank=4, pokemon='mew', usage_pct=35.13163, raw_usage=5353, raw_pct=34.837, real=4247, real_pct=36.525, date='2022-06', tier='monopsychic')]
```

#### `pokemon_usage` → usage statistics for a single Pokémon

```python
from smog_usage_stats import Metagame, pokemon_usage

result = pokemon_usage(Metagame(2022, 11, 8, tier="ou"), "scIzor")
```

```
Usage(rank=44, pokemon='scizor', usage_pct=3.50114, raw_usage=67725, raw_pct=3.565, real=51565, real_pct=3.44, date='2022-11', tier='gen8ou')
```

Returns `None` if the Pokémon doesn't appear in that month's stats. Names ignore case and spaces, so `"Iron Valiant"` and `"ironvaliant"` both work.

#### `chaos_stats` → detailed "Chaos" data for a single Pokémon

The chaos data covers moves, items, abilities, spreads, teammates, checks and counters, and more.

```python
from smog_usage_stats import Metagame, chaos_stats

result = chaos_stats(Metagame(2022, 7, 8, tier="uu"), "SKARMORY")
```

```
{'Moves': {'drillpeck': 375.2124391148, 'tailwind': 208.4057975296,
'swordsdance': 178.0771715149, 'toxic': 1946.992820672, ...},
'Checks and Counters': ... (truncated) }
```

It works the same way for monotype:

```python
result = chaos_stats(Metagame(2022, 11, 9, mono_type="fairy"), "Gardevoir")
```

```
{'Moves': {'calmmind': 15.5, 'moonblast': 16.0, 'psychic': 14.0, ...},
'Abilities': {'synchronize': 3.5, 'trace': 19.5},
'Items': {'choicescarf': 7.5, 'adrenalineorb': 7.0, 'rockyhelmet': 4.0, ...},
'Teammates': {'Mimikyu': 17.5781579769, 'Hatterene': 13.3468947861, ...},
'Raw count': 46, ... (truncated) }
```

Returns `None` if the Pokémon isn't in that month's data.

#### Rating cutoffs

Every lookup uses the 1500 rating cutoff by default. Pass `rating` to use one of Smogon's other cutoffs:

```python
usage_stats(Metagame(2022, 6, 8, tier="ou"), rating=1825)
```

#### Handling errors

All errors raised by the package inherit from `SmogonError`, so one `except` catches everything:

```python
from smog_usage_stats import Metagame, SmogonError, usage_stats

try:
    results = usage_stats(Metagame(2022, 6, 8, tier="ou"))
except SmogonError as error:
    print(f"Couldn't get stats: {error}")
```

Or catch them individually:

| Error | Raised when |
|---|---|
| `InvalidFormatError` | The year, month, generation, tier or type can't exist on Smogon |
| `PageNotFound` | The request is valid, but Smogon has no file for it |
| `QueryError` | Smogon couldn't be reached, or returned an error |

### Command line

The package also installs a `smog-usage-stats` command. Use `--help` to see every command and option:

```
smog-usage-stats --help
smog-usage-stats search --help
```

Search a metagame by year, month, generation and tier (the tier defaults to `ou`):

```
smog-usage-stats search 2022 6 8 ou
```

Search a monotype metagame by year, month, generation and type:

```
smog-usage-stats monotype 2022 6 8 psychic
```

Save the results with `--save-to` (a folder) and `--save-as` (`csv`, `json` or `sql`; the default is `csv`):

```
smog-usage-stats search 2022 6 8 ou --save-to data --save-as json
```

This creates `data/gen8ou_2022_06.json`.

Other options:

```
smog-usage-stats --version
smog-usage-stats --repo
```

### Upgrading from 1.x

The old classes (`BaseStatsSearch`, `MonotypeStatsSearch`, `BaseChaosSearch` and `MonotypeChaosSearch`) still work exactly as before, so existing code doesn't need changing. They're deprecated and will be removed in a future release. Here's how they map to the new functions:

```python
# Before
from smog_usage_stats import usageStats
search = usageStats.BaseStatsSearch(2022, "06", 8, "ou")
results = search.search()

# After
from smog_usage_stats import Metagame, usage_stats
results = usage_stats(Metagame(2022, 6, 8, tier="ou"))
```

## Contributing:

If you find a bug, please [make an issue](https://github.com/Stu-Gotz/smog_usage_stats/issues).

If you would like to contribute, feel free to create a fork and submit a pull request.

## License

MIT License

## Thanks

Thanks to Kaggle user Cristobal Mitchell for the Pokedex dataset.
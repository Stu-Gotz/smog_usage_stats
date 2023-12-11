# smog_usage_stats

A Python wrapper for interacting with Smogon's Pokemon Showdown usage stats data [found here](https://smogon.com/stats) and making it accessible in usable data structures.

## Quick Rundown

### Installing:

`pip install smog-usage-stats`

If your system uses `pip3` instead of `pip`, use that.

### How it all works

`BaseStatsSearch` -> Retrieves metagame usage statistics for non-Monotype metagames.

    smog_usage_stats.UsageStatsLookup as smog
    
    baseSearch = smog.BaseStatsSearch(2022, '06', 8, 'ou')
    results = baseSearch.search()
    # returns 2-D array

`MonotypeStatsSearch` -> searches the monotype stats directory

[[ Example here ]]

`BaseChaosSearch` -> searches the chaos data contained within a certain months stats
data

[[ Example here ]]

`MonotypeChaosSearch` -> searches the monotype chaos data contained within a certain
months stats data

[[ Example here ]]


`IndividualStatsSearch`  -> 
[[ Example here ]]


[[]]


## Contributing:

If you find a bug, please [make an issue](https://github.com/Stu-Gotz/smog_usage_stats/issues). 

If you would like to contribute, feel free to create a fork and submit a pull request.

## License

MIT License

Copyright (c) 2023 Stu-Gotz 

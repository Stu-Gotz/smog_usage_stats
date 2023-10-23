# smog_usage_stats

This is a bit of a pet project of mine that has been in the works for some while and
seen several iterations.

In short, it pulls usage stats from [smogon.com's stats
pages](https://smogon.com/stats) and turns them into a usable data. Originally, it
was a very functional solution, currently I am working to shift it to OOP and once
that's sorted, ship it as a package so other people can use it.

## Quick Rundown

### Installing:

Because its not a package yet, you will have to download this to somewhere on your
PC. Just download it the same way you normally copy code repositories from Git. Open
it in your favourite IDE or text editor and have fun.

### How it all works

`Search.py` is the uber parent searcher class, that all other searcher classes
inherit from. You shouldn't need to ever call this directly.

The four primary search classes are:

`BaseStatsSearch` -> searches the normal stats directory

`MonotypeStatsSearch` -> searches the monotype stats directory

`BaseChaosSearch` -> searches the chaos data contained within a certain months stats
data

`MonotypeChaosSearch` -> searches the monotype chaos data contained within a certain
months stats data

The latter two are more individual searches and there is also a (WIP)
`IndividualStatsSearch` class which will be used to search for individual usage stats
data from the Base or Monotype stats search classes.

`Validation.py` handles the validation of query parameters for the queries, making
sure everything is lined up to actually return data. The first instance of this
project had a very shotgun-blast approach which was massively ineffective and did not
account for discrepencies in labeling conventions used by Smogon in their earlier
days of stats collection. You also should never need to call this directly, it is
effectively a helper class.

`SQLInterface.py` does what it says on the tin, it allows interacting with a (in
this case) PostgreSQL database instance. I HIGHLY recomend using a .env file if you
use this in any way, and add it to your `.gitignore`.

`Update.py` is a class to push new data to the database. The SQL data serves as a
backend for a full-stack application I am working on as well, so it's probably not
necessary for this nor `SQLInterface.py` to be used for most cases, but it is there
if someone maybe wants to make a Mongo interface or anything else.

## Future plans:

- Finish up individual stats search
- Clean up directory to get rid of old data
- Test test test
- Write update function to work as a scheduled task

## Contributing:

If you find a bug, please make
an issue and then submit a pull request when it's sorted.

If you are interested in just using this on your own, feel free to copy and make
changes as you like, it's not owned by me, just a fun project. I'll add in licensing
stuff once I package it up, but it will always be open-source.

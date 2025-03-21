# Welcome to the Dev README.

Thank you for visiting. I'm very amateur and casual so sorry in advance for
that. I assume you are here because you in some way find this interesting and
want to help contribute. For that we salute you. I'm keeping everything at
80 characters, for you terminal troopers.

# The Many Things To Do

In no particular order, this is some things I think I want to get done, get
fixed or get implemented.

## Actual Code Changes

## Code Style

Follow all the PEP stuff and that. Keep it obvious, keep it simple, keep it as
clean as possible and keep it coherent.

I think as it stands it's pretty chaotic, but some things I like:
(Nothing is written in stone.)

`TitleCase` for classes

`camelCase` for Methods

`snake_case` for internal variables

`"strings"` in double quotes

`'a'` character goes in single quotes

This is just kinda my own preference, but I think it's also already pretty much
follows these already or I will fix them as I scan.

## Explaining my schizophrenic code

So I kinda just started this as a way to understand inheretance and polymorphism
and overriding and all that good stuff, and was something I started many many
moons ago when I was just learning how to use Python and it's been a fraught and
chaotic journey. Feel free to browse the commits and witness the evolution of
ignorant to mediocre.

### `search.py`

[search.py](/src/smog_usage_stats/search.py) is the, for lack of a better word, progenator class, `_Search`.
Its really just a means to store commonly used methods across its many child
classes.

(Author: At the moment I have under-prefixed it, because it shouldn't really be
used outside it's children. I realise this is probably a bit odd, but I'm kinda
new here so I don't know everything.)

### `usageStats.py`

[usageStats.py](/src/smog_usage_stats/usageStats.py) allows a user to interact with
the Smogon usage stats with `BaseStatsSearch` and `MonotypeStatsSearch`. The
various private methods focus mostly on formatting data and handling edge cases.
`search()` and `individual_lookup()` allow a user to either do a batch lookup or
search a for an individual Pokémon's usage stat data.

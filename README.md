# smog_usage_stats
Smogon usage stats retriever

The whole goal of this is to make an API that is stable and creates organised, neat, usage stats. There is _a lot_ of work to do still, this was just like a little something I threw together way back in my nascent days of learning python and sql and seemed like a good use case to get comfortable. This is public and since it ain't shit right now, anyone is free to work on it and help out, but I would appreciate just sending a pull request so it becomes kind of a community effort, rather than just one lonely nerd or a bunch of lonely nerds working independently. Many hands make light work. 

# Todo: 
(feel free to discuss this) in the issues or send an email through git.

1. Write better code for the data pull thing.
    - re-organise the data structure to include the held items/teammates thing (not sure if its better to include them in the same tables, or to put them in separate tables and pull it off an id key
    
2. Setup to autorun on the 3nd of every month (since the pages probably get hit pretty hard when new stats are released, want to give a breather before the pull).

3. Write some javascript API that can be used to retrieve the data in a format similar to this https://smogon-usage-stats.herokuapp.com/ since it appears to no longer be worked on, and I can't find any repo it was stored in to take it up from there.

4. I guess that's the big picture, should be broken down more, probably.

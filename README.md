# smog_usage_stats
Smogon usage stats retriever

The whole goal of this is to make an API that is stable and creates organised, neat, usage stats. There is _a lot_ of work to do still, this was just like a little something I threw together way back in my nascent days of learning python and sql and seemed like a good use case to get comfortable. This is public and since it ain't shit right now, anyone is free to work on it and help out, but I would appreciate just sending a pull request so it becomes kind of a community effort, rather than just one lonely nerd or a bunch of lonely nerds working independently. Many hands make light work. 

Currently able to:

Connect to smogon, can get data in json or csv values, depending on what flavour you like. 
*!Currently database only works on CSV files!*
Can build a database, based on dates selected.

# Use:

The whole thing isn't done yet. Currenly only `smogon_pull.py` and `DBManager.py` are worth a damn. I should probably move them out, but then I have to redo all the path settings, and that's a bit of a ballache.

 - with smogon_pull:
 ```
 import smogon_pull
 
 cs = smogon_pull.Contact_Smogon(years: list, months: list, gens: list, tiers: list, ratings: list, mono: bool, monotype: str)
 cs.find_stats(output_type: str) #"csv" or "json"
 ```
This will create a `data/csv/` or `data/json/` folder containing the usage stats. I realise with a lot of dates, this can take up a lot of hd space. Eventually they will be `.zip` files and it will go from there, but for the time being, this is good enough because my pc has enough space on it to be viable. Feel free to make a modification to it if it's needed. A zip file from mid 2020 to the earliest possible date (2014 sometime) is about 30mb zipped of CSVs.

To do the POSTGRES part:

```
import os
import DBManager

#if you need to change your database/username/password/host/port, do DBManager.<one of those in all caps>
current = os.getcwd()
directory = os.path.join(current, "data/csv")
dirlist = os.listdir(directory)

manager = DBManager.DB_Manager(dirlist: list) #list of files in the data/csv/ directory, or wherever if they are in another place
manager.construct_tables()
manager.fill_tables()
manager.close_db()
```

# Next steps: 
(feel free to discuss this) in the issues or send an email through git.

1. Work on leads (easy win, since it's roughly the same).

2. Work on movesets (this is a ballache).
2a. Work on monotype (easy win, create `if/elif` in requests section). Also do leads and movesets for monotype
3. Megas stats? Not sure if it's even relevant.

4. Gui? I don't know if I want to make this a full fledged thing yet. Guess I may as well, but want to finish the webapp I started first. Also I hate guis so if anyone feels like forking and making one, that would be dope af.

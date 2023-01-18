# smog_usage_stats
Smogon usage stats retriever

The whole goal of this is to make an API that is stable and creates organised, neat, usage stats. There is _a lot_ of work to do still, this was just like a little something I threw together way back in my nascent days of learning python and sql and seemed like a good use case to get comfortable. ~~This is public and since it ain't shit right now, anyone is free to work on it and help out, but I would appreciate just sending a pull request so it becomes kind of a community effort, rather than just one lonely nerd or a bunch of lonely nerds working independently. Many hands make light work.~~ I may be using this for school, so I can't accept help in the form of actual code contributions, but I can accept advice which is always appreciated.

Currently able to:

Connect to smogon, can get data in json or csv values, depending on what flavour you like. 
*!Currently database only works on CSV files!*
Can build a database, based on dates selected.

# Use:

Eventually I will probably turn the smogon pull thing into its own little library so someone has the option to just create a fuckload of CSVs, and keep the database separate. On verra.

### Smogon pull

```
from smogon_pull import Contact_Smogon
 
cs = Contact_Smogon(years: list, months: list, gens: list, tiers: list, ratings: list, mono: bool, monotype: str)
cs.find_stats("csv")
```
This will create a `data/csv/` or `data/json/` folder containing the usage stats. I realise with a lot of dates, this can take up a lot of hd space. Eventually they will be `.zip` files and it will go from there, but for the time being, this is good enough because my pc has enough space on it to be viable. Feel free to make a modification to it if it's needed. A zip file from mid 2020 to the earliest possible date (2014 sometime) is about 30mb zipped of CSVs.

### To do the POSTGRES part:
(its a little more involved)
```
#in DBManager.py
# -------------------------------
# Connection to database
# -------------------------------
# Server connection
!v COMMENT OUT THESE TWO LINES v
db_url = os.environ.get("DATABASE_URL")
CONN = pg2.connect(db_url, sslmode="require")

!v UNCOMMENT OUT THESE LINES AND FILL WITH YOUR DB INFO / .env VARIABLES v
# Local connection
# CONN = pg2.connect(
#     database = os.environ.get('LOCAL_DATABASE'),
#     user     = os.environ.get('LOCAL_USER'),
#     password = os.environ.get('LOCAL_PASSWORD'),
#     host     = os.environ.get('LOCAL_HOST'),
#     port     = os.environ.get('LOCAL_PORT')
# )
```


# What's Next?: 
An actual todo list, with gusto.
(Also kind of a stream of conciousness for planning)

Things I would like:
- MORE EFFICIENT PARSER
- trim down date range maybe for database to be smaller and therefore faster to search on API end
  - less information but honestly less herculean task
- Monotype branching (relatively easy, add /monotype/ after date-tier)
  - new table for database (monotype)
  - new options to add as features for api (just add /mono/ to url)
  - new toggle feature for UI (would like the sliding radio button)
- moveset
  - create new python file
  - parsing will be a pain in the cock (NOTE TO SELF MAKE SOME OF THESE CHANGES FOR EXISTING PARSER)
    - (need something like a sliding window to grab keywords)
    - list of every pokemon name to search as keyword too (many iterations)
    - split values on number, into tuples
    - trim whitespace, trim % signs
    - im sure ill find something else once i start
  - will also have to be done for monotype branches
    - IDEA: split off into two files, one that handles reg search, one for mono
- leads
  - same as above but easier time parsing (relative)
  - BONUS: way smaller for monotype


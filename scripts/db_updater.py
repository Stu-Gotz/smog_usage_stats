import smogon_pull as SP
import DBManager as DBM

# SP.update()
_DBM = DBM.SQLManager()
_DBM.connect(db_name="UsageStats")
_DBM.update_tables()
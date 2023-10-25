import smogon_pull as SP
import deprecated.DBManager as DBM

# SP.update()
_DBM = DBM.SQLManager()
_DBM.connect(db_name="UsageStats")
_DBM.update_tables()
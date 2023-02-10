#import smogon_pull as SP
import DBManager as DBM

#SP.update()
_DBM = DBM.DB_Manager()
_DBM.construct_tables()
_DBM.fill_tables()
_DBM.close_db()

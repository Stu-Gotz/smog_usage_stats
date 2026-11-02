# ------------------------
# Utility and shorthand functions
# ------------------------
import datetime


def strfym(ymstr: str):
    datetime.strptime(ymstr, "%Y-%m")

from typing import Literal
from os.path import dirname as up
import os
import shutil
from datetime import datetime

#"Mega"-parent searching class. Everything contained within this class will be available,
#but not necessarily used by child classes.
class Search:
    '''
    Parent searcher class.
        Params:
            year (str or int): a string or integer year
            month (str): two-digit string month
            gen: (str or int): an integer for whichever Pokemon generation is being queried. 
    '''
    def __init__(
        self,
        year: str | int,
        month: Literal["Must be a two digit month string eg: '01' for January"],
        gen: str | int,
    ) -> None:
        self.year = year
        self.month = month
        self.date = datetime.strptime(("-".join([str(year), month])), "%Y-%m")
        self.gen = gen
        self.base = 'https://www.smogon.com/stats/'

    @property
    def year(self) -> str | int:
        return self._year

    @property
    def month(self) -> str:
        return self._month

    @property
    def gen(self) -> str | int:
        return self._gen

    @year.setter
    def year(self, value):
        self._year = value

    @month.setter
    def month(self, value):
        self._month = value

    @gen.setter
    def gen(self, value):
        self._gen = value

    def create_validation_object(self):
        this = vars(self)
        validation_object = {k.replace("_", ""): v for k, v in this.items()}
        return validation_object

    def locate_cache_dir(self, reference):
        base_dir = up(up(reference))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        return cache_dir

    @staticmethod
    def clear_cache():
        base_dir = up(up(__file__))
        # set up the cached dir, theres probably a better way to do this but for now it will suffice
        cache_dir = os.path.join(base_dir, "data\\cache")
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)

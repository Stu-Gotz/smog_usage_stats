import os
import time
import json
import requests
from datetime import datetime
import pandas as pd

class BaseStatsSearch:
    def __init__(self, 
                 years: list, 
                 months: list, 
                 gens: list, 
                 tiers: list):
        self.years = years
        self.months = months
        self.gens = gens
        self.tiers = tiers
    
    @property
    def years(self):
        return self._years
    @property
    def months(self):
        return self._months
    @property
    def gens(self):
        return self._gens
    @property
    def tiers(self):
        return self._tiers
    
    @years.setter
    def years(self, value):
        self._years = value
    @months.setter
    def months(self, value):
        self._months = value
    @gens.setter
    def gens(self, value):
        self._gens = value
    @tiers.setter
    def tiers(self, value):
        self._tiers = value

class MonotypeStatSearch(BaseStatsSearch):
    def __init__(self):
        super().__init__()
        self.base = "https://www.smogon.com/stats/2022-11/chaos/"
    
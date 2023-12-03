import pytest
import requests
import os
from ..src.smog_usage_stats import UsageStatsLookup

base_search = UsageStatsLookup.BaseStatsSearch(year='2023', month='06', gen=9, tier='ou')
print(base_search.year)
# from smog_usage_stats import UsageStatsLookup



@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    def stunted_get():
        raise RuntimeError("Network access not allowed during testing!")
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

@pytest.fixture(autouse=True)
def sample_return_data():
        
    sample_data = open(os.path.join(os.path.abspath(r'tests\\2023-09_gen9ou_test.csv')))
    return [[x for x in sample_data.readlines()]]

@pytest.fixture
def basic_stats_search():
    # base_search = smog_usage_stats.UsageStatsLookup.BaseStatsSearch(year='2023', month='06', gen=9, tier='ou')
    return base_search
    # return BaseStatsSearch(year='2023', month='06', gen=9, tier='ou')
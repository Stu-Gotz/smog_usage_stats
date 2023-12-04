import pytest
import datetime


def test_basic_search_year(basic_stats_search):
    assert basic_stats_search.year == "2023"


def test_basic_search_month(basic_stats_search):
    assert basic_stats_search.month == "06"


def test_basic_search_tier(basic_stats_search):
    assert basic_stats_search.tier == "ou"


def test_basic_search_gen(basic_stats_search):
    assert basic_stats_search.gen == 9


def test_basic_search_validation_object(basic_stats_search):
    assert basic_stats_search._create_validation_object() == {
        "year": "2023",
        "month": "06",
        "date": datetime.datetime(2023, 6, 1, 0, 0),
        "gen": 9,
        "base": "https://www.smogon.com/stats/2023-06/gen9ou-1500.txt",
        "isMonotype": False,
        "ending": "gen9ou-1500.txt",
        "tier": "ou",
    }

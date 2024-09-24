import pytest
import datetime


def test_mono_search_year(mono_stats_search):
    assert mono_stats_search.year == "2023"


def test_mono_search_month(mono_stats_search):
    assert mono_stats_search.month == "09"


def test_mono_search_typing(mono_stats_search):
    assert mono_stats_search.typing == "psychic"


def test_mono_search_gen(mono_stats_search):
    assert mono_stats_search.gen == 9

def test_mono_search_url(mono_stats_search):
    assert mono_stats_search.base == "https://www.smogon.com/stats/2023-09/monotype/gen9monotype-monopsychic-1500.txt"

def test_is_monotype(mono_stats_search):
    assert mono_stats_search.isMonotype == True

def test_monotype_individual_lookup(sample_monotype_data, mono_stats_search):
    mono_stats_search.result = sample_monotype_data
    res = mono_stats_search.individual_lookup("jirachi") 
    assert res == ['9', 'jirachi', '21.54879', '1742', '21.241', '1398', '23.312', '2023-09', 'monopsychic\n']

def test_mono_search_validation_object(mono_stats_search):
    assert mono_stats_search._create_validation_object() == {
        "year": "2023",
        "month": "09",
        "date": datetime.datetime(2023, 9, 1, 0, 0),
        "gen": 9,
        "base": "https://www.smogon.com/stats/2023-09/monotype/gen9monotype-monopsychic-1500.txt",
        "ending": "gen9monotype-monopsychic-1500.txt",
        "isMonotype": True,
        "typing": "psychic",
    }

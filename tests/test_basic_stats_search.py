import pytest

def test_basic_search_year(basic_stats_search):
    assert basic_stats_search.year == '2023'

def test_basic_search_month(basic_stats_search):
    assert basic_stats_search.month == '06'

def test_basic_search_tier(basic_stats_search):
    assert basic_stats_search.tier == 'ou'

def test_basic_search_gen(basic_stats_search):
    assert basic_stats_search.gen == 9
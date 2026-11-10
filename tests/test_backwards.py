import csv

import pytest

from smog_usage_stats import InvalidFormatError
from smog_usage_stats.transformer import COLUMNS

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


@pytest.fixture
def base_search():
    from smog_usage_stats import usageStats

    return usageStats.BaseStatsSearch(year="2023", month="09", gen=9, tier="ou")


@pytest.fixture
def mono_search():
    from smog_usage_stats.usageStats import MonotypeStatsSearch

    return MonotypeStatsSearch(year="2023", month="09", gen=9, typing="psychic")


def test_old_attributes(base_search):
    assert base_search.year == "2023"
    assert base_search.month == "09"
    assert base_search.gen == 9
    assert base_search.tier == "ou"
    assert base_search.isMonotype is False
    assert base_search.base == "https://www.smogon.com/stats/2023-09/gen9ou-1500.txt"
    assert str(base_search) == base_search.base
    assert base_search.ending == "gen9ou-1500.txt"


def test_old_monotype_attributes(mono_search):
    assert mono_search.typing == "psychic"
    assert mono_search.isMonotype is True
    assert mono_search.base == (
        "https://www.smogon.com/stats/2023-09/monotype/gen9monotype-monopsychic-1500.txt"
    )


def test_search_matches_csv_exactly(base_search, fake_smogon, expected_ou):
    result = base_search.search()

    assert fake_smogon == [base_search.base]
    assert result == expected_ou
    assert base_search.result is result


def test_monotype_search_matches_csv(mono_search, expected_mono):
    result = mono_search.search()
    assert result[: len(expected_mono)] == expected_mono


def test_individual_lookup(base_search, fake_smogon):
    with pytest.raises(ValueError):
        base_search.individual_lookup("greattusk")

    base_search.search()
    assert base_search.individual_lookup("greattusk")[:2] == ["1", "greattusk"]
    assert base_search.individual_lookup("Iron Valiant")[1] == "ironvaliant"
    assert base_search.individual_lookup("pikachu") is None


def test_chaos_searches(fake_smogon):
    from smog_usage_stats import chaosStats

    base = chaosStats.BaseChaosSearch("2023", "09", 9, name="Great Tusk", tier="ou")
    assert base.name == "great tusk"
    assert base.base == "https://www.smogon.com/stats/2023-09/chaos/gen9ou-1500.json"
    assert base.search()["Raw count"] == 1143813
    assert fake_smogon == [base.base]

    mono = chaosStats.MonotypeChaosSearch(
        "2023", "09", 9, name="hatterene", typing="psychic"
    )
    assert mono.base == (
        "https://www.smogon.com/stats/2023-09/monotype/chaos/gen9monotype-monopsychic-1500.json"
    )


def test_chaos_search_missing_pokemon_returns_none(fake_smogon):
    from smog_usage_stats.chaosStats import BaseChaosSearch

    assert BaseChaosSearch(2023, "09", 9, name="Pikachu", tier="ou").search() is None


@pytest.mark.filterwarnings("default::DeprecationWarning")
def test_old_classes_warn():
    from smog_usage_stats.usageStats import BaseStatsSearch

    with pytest.warns(DeprecationWarning, match="usage_stats"):
        BaseStatsSearch("2023", "09", 9, "ou")

import pytest

from smog_usage_stats import (
    Formatter,
    InvalidFormatError,
    PageNotFound,
    extended_stats,
    single_stats,
    usage_stats,
    usage_url,
)
from smog_usage_stats.transformer import parse_chaos

OU = Formatter(2023, 9, 9, tier="ou")
MONO = Formatter(2023, 9, 9, mono_type="psychic")


def assert_matches_csv(rows, expected_csv):
    header, *expected = expected_csv
    assert list(rows[0].as_dict()) == header
    for row, expected_row in zip(rows, expected):
        for value, expected_value in zip(row.as_dict().values(), expected_row):
            if isinstance(value, float):
                assert value == pytest.approx(float(expected_value))
            else:
                assert str(value) == expected_value


# --- Format ---------------------------------------------------------------


def test_inputs_are_normalized():
    fmt = Formatter("2023", "09", "9", tier="OU")
    assert (fmt.year, fmt.month, fmt.gen, fmt.tier) == (2023, 9, 9, "ou")
    assert fmt.period == "2023-09"


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(year=2014, month=10, gen=6, tier="ou"),  # before stats exist
        dict(year=2022, month=6, gen=9, tier="ou"),  # before gen 9
        dict(year=2023, month=13, gen=9, tier="ou"),  # not a month
        dict(year=2023, month=9, gen=9, mono_type="cosmic"),  # not a type
        dict(year=2023, month=9, gen=9),  # neither tier nor type
    ],
)
def test_invalid_formats_raise(kwargs):
    with pytest.raises(InvalidFormatError):
        Formatter(**kwargs)


def test_november_2014_is_valid():
    Formatter(2014, 11, 6, tier="ou")  # the 1.x validator rejected this


# --- Usage stats ----------------------------------------------------------


def test_usage_urls():
    assert usage_url(OU) == "https://www.smogon.com/stats/2023-09/gen9ou-1500.txt"
    assert usage_url(MONO) == (
        "https://www.smogon.com/stats/2023-09/monotype/gen9monotype-monopsychic-1500.txt"
    )


def test_usage_stats_matches_csv(fake_smogon, expected_ou):
    rows = usage_stats(OU)
    assert fake_smogon == [usage_url(OU)]
    assert len(rows) == len(expected_ou) - 1
    assert_matches_csv(rows, expected_ou)


def test_monotype_usage_stats_matches_csv(expected_mono):
    rows = usage_stats(MONO)
    assert len(rows) == 46  # the CSV only holds the first 28 of these
    assert_matches_csv(rows, expected_mono)


def test_usage_values_are_typed():
    first = usage_stats(OU)[0]
    assert first.rank == 1 and isinstance(first.usage_pct, float)


def test_pokemon_usage():
    assert single_stats(OU, "Iron Valiant").rank == 3
    assert single_stats(OU, "Pikachu") is None


def test_missing_file_raises_not_found():
    with pytest.raises(PageNotFound):
        usage_stats(Formatter(2023, 9, 9, tier="uu"))  # no fixture -> fake 404


# --- Chaos stats ----------------------------------------------------------


def test_extended_stats(fake_smogon, chaos_ou):
    tusk = extended_stats(OU, "great tusk")
    assert fake_smogon == [
        "https://www.smogon.com/stats/2023-09/chaos/gen9ou-1500.json"
    ]
    assert tusk == chaos_ou["data"]["Great Tusk"]
    assert "headlongrush" in tusk["Moves"]


def test_extended_stats_missing_pokemon():
    assert extended_stats(OU, "Pikachu") is None


def test_parse_chaos_ignores_case_and_spaces(chaos_ou):
    assert parse_chaos(chaos_ou, "IRONVALIANT") == chaos_ou["data"]["Iron Valiant"]

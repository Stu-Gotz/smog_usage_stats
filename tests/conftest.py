import csv
import json
from pathlib import Path

import pytest
import requests

from smog_usage_stats import query

TESTS = Path(__file__).parent
STATS = "https://www.smogon.com/stats"

# Which local file stands in for which Smogon URL.
FAKE_SMOGON = {
    f"{STATS}/2023-09/gen9ou-1500.txt": TESTS / "2023-09_gen9ou-1500.txt",
    f"{STATS}/2023-09/monotype/gen9monotype-monopsychic-1500.txt": TESTS
    / "2023-09-mono-psychic-test.txt",
    # Hand-made: same structure as Smogon's chaos files, but invented numbers.
    f"{STATS}/2023-09/chaos/gen9ou-1500.json": TESTS / "2023-09_gen9ou-1500.json",
}


def _fake_response(url: str) -> requests.Response:
    """A real requests.Response, so .ok, .text and .json() all behave normally.

    URLs not in FAKE_SMOGON get a 404, the same as a missing page on Smogon.
    """
    response = requests.Response()
    response.url = url
    response.encoding = "utf-8"
    path = FAKE_SMOGON.get(url)
    if path is None:
        response.status_code = 404
        response._content = b"Not Found"
    else:
        response.status_code = 200
        response._content = path.read_bytes()
    return response


@pytest.fixture(autouse=True)
def fake_smogon(monkeypatch):
    """Serve local files for Smogon URLs. Returns the list of URLs requested,
    so tests can check that the right URL was built."""
    requested = []

    def fake_get(url, *args, **kwargs):
        requested.append(url)
        return _fake_response(url)

    def no_network(*args, **kwargs):
        raise RuntimeError(
            "Network access isn't allowed in tests. Add a fixture to FAKE_SMOGON."
        )

    monkeypatch.setattr(query._session, "get", fake_get)
    # Safety net
    monkeypatch.setattr(requests.Session, "request", no_network)
    return requested


def _read_csv(name: str) -> list[list[str]]:
    with open(TESTS / name, newline="") as file:
        return list(csv.reader(file))


@pytest.fixture
def expected_ou():
    """The formatted gen9ou output: a header row, then every Pokemon."""
    return _read_csv("2023-09_gen9ou_test.csv")


@pytest.fixture
def expected_mono():
    """The formatted monopsychic output: a header row, then the first 28 Pokemon."""
    return _read_csv("2023-09-mono-psychic-test.csv")


@pytest.fixture
def chaos_ou():
    with open(TESTS / "2023-09_gen9ou-1500.json") as file:
        return json.load(file)

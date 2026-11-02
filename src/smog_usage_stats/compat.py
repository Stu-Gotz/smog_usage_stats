# From claude, backwards compatibility port.

from __future__ import annotations

from . import api
from .formatting import Formatter
from .transformer import USAGE_COLUMNS


def _as_lists(rows) -> list[list]:
    """The old return shape: a header row, then one list per Pokemon."""
    return [USAGE_COLUMNS] + [list(row.as_dict().values()) for row in rows]


class BaseStatsSearch:
    def __init__(self, year, month, gen, tier):
        self.format = Formatter(year, month, gen, tier=tier)

    def search(self) -> list[list]:
        return _as_lists(api.usage_stats(self.format))


class MonotypeStatsSearch:
    def __init__(self, year, month, gen, typing):
        self.format = Formatter(year, month, gen, mono_type=typing)

    def search(self) -> list[list]:
        return _as_lists(api.usage_stats(self.format))


class BaseChaosSearch:
    def __init__(self, year, month, gen, name, tier):
        self.format = Formatter(year, month, gen, tier=tier)
        self.name = name

    def search(self) -> dict | None:
        return api.chaos_stats(self.format, self.name)


class MonotypeChaosSearch:
    def __init__(self, year, month, gen, name, typing):
        self.format = Formatter(year, month, gen, mono_type=typing)
        self.name = name

    def search(self) -> dict | None:
        return api.chaos_stats(self.format, self.name)

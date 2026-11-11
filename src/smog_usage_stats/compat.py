# From claude, backwards compatibility port.

from __future__ import annotations

import os
import csv
import shutil
import warnings

from . import api, query
from .formatting import Metagame
from .transformer import COLUMNS, normalise_name, parse_usage, parse_chaos


def _as_lists(rows) -> list[list]:
    """The old return shape: a header row, then one list per Pokemon."""
    return [COLUMNS] + [list(row.as_dict().values()) for row in rows]


def _warn(old: str, new: str) -> None:
    warnings.warn(
        f"{old} is deprecated and will be removed in 2.0. Use {new} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


class StatsSearch:
    """Shared behavior of BaseStatsSearch and MonotypeStatsSearch."""

    format: Metagame

    def __init__(self, year, month, gen):
        # 1.x kept year and month exactly as passed, and converted gen to int.
        self.year = year
        self.month = month
        self.gen = int(gen)
        self.result = None
        self.base = api.usage_url(self.format)
        self.ending = self.base.rsplit("/", 1)[-1]

    @property
    def isMonotype(self) -> bool:
        return self.format.is_monotype

    def __str__(self) -> str:
        return self.base

    def search(self) -> list[list[str]]:
        """A header row, then one row of strings per Pokemon, as in 1.x."""
        text = query.get_text(self.base)
        rows = [
            [
                rank,
                normalise_name(name),
                *numbers,
                self.format.period,
                self.format.label,
            ]
            for rank, name, *numbers in parse_usage(text)
        ]
        self.result = [list(COLUMNS)] + rows
        return self.result

    def individual_lookup(self, name: str) -> list[str] | None:
        if not self.result:
            raise ValueError("No search results found. Call search() first.")
        wanted = normalise_name(name)
        return next((row for row in self.result[1:] if row[1] == wanted), None)

    # def search_and_save(self, pathname: str | os.PathLike | None = None) -> None:
    #     """Save to ./smogon_cache[/pathname]/<year>-<month>_<metagame>.csv"""
    #     data = self.search()
    #     if len(data) < 2:
    #         return None  # 1.x wrote a file, then deleted it, if there was no data
    #     folder = os.path.join(
    #         os.getcwd(), "smogon_cache", *([pathname] if pathname else [])
    #     )
    #     os.makedirs(folder, exist_ok=True)
    #     # 1.x named monotype files just "gen9monotype", so every type overwrote
    #     # the same file. The full slug keeps them apart.
    #     filename = f"{self.year}-{self.month}_{self.ending.rsplit('-', 1)[0]}.csv"
    #     with open(os.path.join(folder, filename), "w", newline="") as file:
    #         csv.writer(file).writerows(data)

    # @staticmethod
    # def clear_cache(target: str) -> None:
    #     """Delete a cache folder (relative to the current directory), as in 1.x."""
    #     if os.path.exists(target):
    #         shutil.rmtree(target)


class BaseStatsSearch(StatsSearch):
    def __init__(self, year, month, gen, tier):
        _warn("BaseStatsSearch", "usage_stats(Metagame(year, month, gen, tier=...))")
        self.format = Metagame(year, month, gen, tier=tier)
        self.tier = self.format.tier
        super().__init__(year, month, gen)


class MonotypeStatsSearch(StatsSearch):
    def __init__(self, year, month, gen, typing):
        _warn(
            "MonotypeStatsSearch",
            "usage_stats(Metagame(year, month, gen, mono_type=...))",
        )
        self.format = Metagame(year, month, gen, mono_type=typing)
        self.typing = self.format.mono_type
        super().__init__(year, month, gen)


class ChaosSearch:
    """Shared behavior of BaseChaosSearch and MonotypeChaosSearch."""

    format: Metagame

    def __init__(self, year, month, gen, name):
        self.year = year
        self.month = month
        self.gen = int(gen)
        self.name = name.lower()
        self.base = api.chaos_url(self.format)

    @property
    def isMonotype(self) -> bool:
        return self.format.is_monotype

    def __str__(self) -> str:
        return self.base

    def search(self) -> dict | None:
        return parse_chaos(query.get_json(self.base), self.name)


class BaseChaosSearch(ChaosSearch):
    def __init__(self, year, month, gen, name, tier):
        _warn(
            "BaseChaosSearch",
            "extended_stats(Metagame(year, month, gen, tier=...), name)",
        )
        self.format = Metagame(year, month, gen, tier=tier)
        self.tier = self.format.tier
        super().__init__(year, month, gen, name)


class MonotypeChaosSearch(ChaosSearch):
    def __init__(self, year, month, gen, name, typing):
        _warn(
            "MonotypeChaosSearch",
            "extended_stats(Metagame(year, month, gen, mono_type=...), name)",
        )
        self.format = Metagame(year, month, gen, mono_type=typing)
        self.typing = self.format.mono_type
        super().__init__(year, month, gen, name)

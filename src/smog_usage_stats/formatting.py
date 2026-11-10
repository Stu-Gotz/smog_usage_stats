from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


from .errors import InvalidFormatError

TYPES = frozenset(
    {
        "normal",
        "fire",
        "water",
        "grass",
        "flying",
        "fighting",
        "poison",
        "electric",
        "ground",
        "rock",
        "psychic",
        "ice",
        "bug",
        "ghost",
        "steel",
        "dragon",
        "dark",
        "fairy",
    }
)

FIRST_MONTH = (2014, 11)

MODERN_START = (2017, 11)

CUTOFFS = {
    "7": datetime.strptime("2016-11", "%Y-%m"),
    "8": datetime.strptime("2020-11", "%Y-%m"),
    "9": datetime.strptime("2022-11", "%Y-%m"),
    "10": datetime.strptime(
        "2027-01", "%Y-%m"
    ),  # this will have to be updated to the actual dates when the time comes
}


@dataclass(frozen=True)
class Formatter:
    """A single month of stats per metagame.

    Pass a ``tier`` (e.g. "ou") for standard formats or a ``mono_type``
    (e.g. "grass") for monotype formatss. Inputs are normalized; month=6 and
    month="06" are equivalent."""

    year: int
    month: int
    gen: int
    tier: str | None = None
    mono_type: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "year", int(self.year))
        object.__setattr__(self, "month", int(self.month))
        object.__setattr__(self, "gen", int(self.gen))
        if self.tier is not None:
            object.__setattr__(self, "tier", self.tier.lower())
        if self.mono_type is not None:
            object.__setattr__(self, "mono_type", self.mono_type.lower())
        _validate(self)

    @property
    def period(self) -> str:
        """The "2023-09" part of Smogon's URLs."""
        return f"{self.year}-{self.month:02d}"

    @property
    def is_monotype(self) -> bool:
        return self.mono_type is not None

    @property
    def uses_modern_naming(self) -> bool:
        return (self.year, self.month) >= MODERN_START

    @property
    def slug(self) -> str:
        """The metagame part of the filename, e.g. "gen9ou" or "gen9monotype-monopsychic"."""
        if self.is_monotype:
            return f"gen{self.gen}monotype-mono{self.mono_type}"
        return f"gen{self.gen}{self.tier}"

    @property
    def label(self) -> str:
        """The value used in the "tier" column of results."""
        return f"mono{self.mono_type}" if self.is_monotype else self.slug


# Validator to validate
def _validate(fmt: Formatter) -> None:
    if (fmt.tier is None) == (fmt.mono_type is None):
        raise InvalidFormatError("Pass exactly one of tier= or mono_type=.")
    if not 1 <= fmt.month <= 12:
        raise InvalidFormatError(f"Month {fmt.month} is not between 1 and 12.")
    if (fmt.year, fmt.month) < FIRST_MONTH:
        raise InvalidFormatError(
            f"{fmt.period} is before Smogon's first stats month (2014-11)."
        )
    if fmt.is_monotype and fmt.mono_type not in TYPES:
        raise InvalidFormatError(f"{fmt.mono_type!r} is not a Pokemon type.")
    gen_start = CUTOFFS.get(fmt.gen)
    if gen_start is not None and (fmt.year, fmt.month) < gen_start:
        start_year, start_month = gen_start
        raise InvalidFormatError(
            f"Gen {fmt.gen} has no stats before {start_year}-{start_month:02d}."
        )

from __future__ import annotations

from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup

from .formatting import Metagame


@dataclass(frozen=True)
class Usage:
    rank: int
    pokemon: str
    usage_pct: float
    raw_usage: int
    raw_pct: float
    real: int
    real_pct: float
    date: str
    tier: str

    def as_dict(self) -> dict:
        return asdict(self)


COLUMNS = list(Usage.__dataclass_fields__)


def normalise_name(name: str) -> str:
    return name.replace(" ", "").lower()


def parse_usage(text: str, fmt: Metagame) -> list[Usage]:
    rows = []
    for line in text.splitlines():
        # remove all linebreaks,symbols and make lowercase
        data = [x.strip().rstrip("%") for x in line.split("|")[1:-1]]
        if len(data) != 7 or not data[0].isdigit():
            continue
        rank, name, usage, raw, raw_pct, real, real_pct = data
        rows.append(
            Usage(
                rank=int(rank),
                pokemon=normalise_name(name),
                usage_pct=float(usage),
                raw_usage=int(raw),
                raw_pct=float(raw_pct),
                real=int(real),
                real_pct=float(real_pct),
                date=fmt.period,
                tier=fmt.label,
            )
        )
    return rows


def parse_chaos(data: dict, name: str) -> dict | None:
    entries = {normalise_name(k): v for k, v in data["data"].items()}
    return entries.get(normalise_name(name))


def parse_directory_listing(html: str) -> set[str]:
    """Metagame names from a stats directory page, e.g. {"gen7ou", "ou", ...}."""
    soup = BeautifulSoup(html, "html.parser")
    names = set()
    for anchor in soup.find_all("a"):
        filename = anchor.text.strip()
        if filename.endswith(".txt"):
            names.add(filename.removesuffix(".txt").rsplit("-", 1)[0])
    return names

from __future__ import annotations

import csv
import os

from . import query
from .errors import PageNotFound
from .formatting import Formatter
from .transformer import (
    COLUMNS,
    Usage,
    parse_chaos,
    parse_directory_listing,
    parse_usage,
)

DEFAULT_RATING = 1500


def _folder(fmt: Formatter, kind: str = "") -> str:
    parts = [query.BASE_URL, fmt.period]
    if fmt.is_monotype:
        parts.append("monotype")
    if kind:
        parts.append(kind)
    return "/".join(parts) + "/"


def _handle_slug(fmt: Formatter) -> str:

    if fmt.uses_modern_naming or fmt.is_monotype:
        return fmt.slug
    available = parse_directory_listing(query.get_text(_folder(fmt)))
    if fmt.slug in available:
        return fmt.slug
    if fmt.gen in (6, 7) and fmt.tier in available:
        return fmt.tier
    raise PageNotFound(f"No stats for {fmt.slug} in {fmt.period}.")


def usage_url(fmt: Formatter, rating: int = DEFAULT_RATING) -> str:
    return f"{_folder(fmt)}{_handle_slug(fmt) - {rating}}.txt"


def chaos_url(fmt: Formatter, rating: int = DEFAULT_RATING) -> str:
    return f"{_folder(fmt, 'chaos')}{_handle_slug(fmt) - rating}.json"


def tier_stats(fmt: Formatter, rating: int = DEFAULT_RATING) -> list[Usage]:
    return parse_usage(query.get_text(usage_url(fmt, rating)), fmt)


def single_stats(
    fmt: Formatter, name: str, rating: int = DEFAULT_RATING
) -> Usage | None:
    wanted = name.replace(" ", "").lower()
    return next((row for row in tier_stats(fmt, rating) if row.pokemon == wanted), None)


def chaos_stats(fmt: Formatter, name: str, rating: int = DEFAULT_RATING) -> dict | None:
    return parse_chaos(query.get_json(chaos_url(fmt, rating)), name)


## Again, disabled for packaging, used for myself
# Or whoever wants to enable it individually if you read this much into the repo.

# def save_usage_csv(rows: list[Usage], path: str | os.PathLike) -> None:
#     """Write usage rows to a CSV with a header row. Creates parent folders."""
#     if not rows:
#         raise ValueError("No rows to save.")
#     folder = os.path.dirname(os.fspath(path))
#     if folder:
#         os.makedirs(folder, exist_ok=True)
#     with open(path, "w", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=COLUMNS)
#         writer.writeheader()
#         writer.writerows(row.as_dict() for row in rows)

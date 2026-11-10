from typing import Annotated
import typer
from . import __version__, __app_name__

from .formatting import Formatter
from .transformer import Usage, COLUMNS
from .api import usage_stats

import os
import csv
import json
import sqlite3

from enum import Enum
from dataclasses import fields
from contextlib import closing

app = typer.Typer()

SQL_TYPES = {"int": "INTEGER", "float": "REAL", "str": "TEXT"}


class SaveFormat(str, Enum):
    csv = "csv"
    json = "json"
    sql = "sql"


def _save_usage_csv(rows: list[Usage], path: str | os.PathLike) -> None:
    """Write usage rows to a CSV with a header row. Creates parent folders."""
    if not rows:
        raise ValueError("No rows to save.")
    folder = os.path.dirname(os.fspath(path))
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(row.as_dict() for row in rows)


def _save_usage_json(rows: list[Usage], path: str | os.PathLike) -> None:
    if not rows:
        raise ValueError("No data present.")
    folder = os.path.dirname(os.fspath(path))
    data = [rows.as_dict() for row in rows]
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as file:
        json.dump(data, file)


def _save_usage_sql(
    rows: list[Usage], path: str | os.PathLike, table_name: str
) -> None:
    column_names = COLUMNS

    if not rows:
        raise ValueError("No data present.")
    # Realistically these should never be raised
    # However, it's always good practice to sanitise your database inputs
    # Even if it's wholly local.
    if not table_name.isidentifier():
        raise ValueError(f"Invalid table name: {table_name!r}")
    if not all(col.isidentifier() for col in column_names):
        raise ValueError("Invalid column names.")

    os.makedirs(os.path.dirname(os.fspath(path)), exist_ok=True)

    # ensures columns are properly typed and nobody gets too helpful
    columns = [
        (
            field.name,
            SQL_TYPES[
                field.type if isinstance(field.type, str) else field.type.__name__
            ],
        )
        for field in fields(Usage)
    ]

    # eg. RANK int
    column_definitions = ", ".join(f'"{name}" {sql_type}' for name, sql_type in columns)
    # list of column strings
    column_names = ", ".join(f'"{name}"' for name, _ in columns)
    # ?, ?, ?, ... ?
    placeholders = ", ".join("?" for _ in columns)

    create_db_query = (
        f'CREATE TABLE IF NOT EXISTS "{table_name}" ('
        f'{column_definitions}, PRIMARY KEY ("rank")'
    )

    insert_query = f'INSERT OR REPLACE INTO "{table_name}" ({column_names}) VALUES ({placeholders})'

    # Populate the table, closes automagically
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(create_db_query)
            connection.executemany(
                insert_query,
                ([getattr(row, name) for name, _ in columns] for row in rows),
            )


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__}, v{__version__}")
        raise typer.Exit()


def _repo_callback(value: bool) -> None:
    if value:
        typer.echo("https://www.github.com/stu-gotz/smog_usage_stats")
        raise typer.Exit()


@app.command()
def search(
    year: Annotated[int, typer.Argument(help="Four (4) digit year.")],
    month: Annotated[
        int, typer.Argument(min=1, max=12, help="Integer month e.g. 4 for April.")
    ],
    gen: Annotated[
        int,
        typer.Argument(
            min=1,
            max=9,
            help="Which generation of Pokemon (generations are based on handheld games).",
        ),
    ],
    tier: Annotated[str | None, typer.Argument(help="What tier of battles?")] = "ou",
    save_to: Annotated[
        str | None,
        typer.Argument(
            help="A folder location to save to.",
        ),
    ] = None,
    save_as: Annotated[
        SaveFormat | None,
        typer.Option(
            help="Choose a file format.",
        ),
    ] = "csv",
) -> None:

    target = usage_stats(Formatter(year, month, gen, tier))

    if save_to:
        if save_as == "csv":
            _save_usage_csv(target, save_to)
        elif save_as == "json":
            _save_usage_json(target, save_to)
        elif save_as == "sql":
            _save_usage_sql(target, save_to, f"gen{gen}{tier}_{year}_{month:02d}")
        else:
            raise typer.BadParameter(
                "save_as option must be one of [csv, json or sql]."
            )
    elif save_to and not save_as:
        raise typer.BadParameter(
            "No format identifier chosen. Please pass one of [csv, json or sql] to the save_as parameter."
        )


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Show the applicaion's version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
    repo: Annotated[
        bool | None,
        typer.Option(
            "--repo",
            "-r",
            help="Show the application's repository.",
            callback=_repo_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    return

    # monotype: Annotated[
    #     str,
    #     typer.Argument(help="Monotype (e.g. 'water'). Mutually exclusive with tier."),
    # ],
    # name: Annotated[
    #     str,
    #     typer.Argument(
    #         "Pokemon name if wanting to access data for just a single Pokemon's usage."
    #     ),
    # ],
    # chaos: Annotated[
    #     str,
    #     typer.Argument("Extended usage stats including moves, held items and beyond."),
    # ],  # should probably change 'chaos' to something more meaningful

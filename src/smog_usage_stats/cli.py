from typing import Optional
import typer
from smog_usage_stats import __version__, __app_name__

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__}, v{__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the applicaion's version and exit.",
        callback=_version_callback,
        is_eager=True
    )
) -> None:
    return


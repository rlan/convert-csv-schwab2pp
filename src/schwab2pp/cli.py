#!/usr/bin/env python3
"""CLI wrapper for the conversion.

This module creates a CLI app and validates arguments.
"""

from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from schwab2pp.convert import convert

app = typer.Typer()


@app.command()
def main(
    schwab_csv: Annotated[
        Optional[Path], typer.Argument(help="CSV file from Charles Schwab")
    ] = None,
    pp_csv: Annotated[
        Path,
        typer.Argument(help="Resulting CSV file for Portfolio Performance"),
    ] = Path("pp.csv"),
) -> int:
    """Convert transactions from Charles Schwab for Portfolio Performance.

    Convert a transactions CSV file from Charles Schwab to an equivalent and
    ready-to-import CSV file for Portfolio Performance.
    """
    # Argument validation
    if schwab_csv is None:
        print("Missing input Schwab CSV file")
        return 0
    if not schwab_csv.exists():
        print("Given Schwab CSV file does not exist")
        return 0
    if not schwab_csv.is_file():
        print("Given Schwab CSV file is not a file")
        return 0
    # Argument validation
    if pp_csv.exists():
        print(f"The existing PP CSV file, {str(pp_csv)}, will be overwritten")

    return convert(schwab_csv, pp_csv)


if __name__ == "__main__":
    app()

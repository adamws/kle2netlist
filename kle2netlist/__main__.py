# type: ignore[attr-defined]

from typing import Optional

import json
import random
from enum import Enum

import typer
from kle2netlist import __version__
from kle2netlist.skidl import kle2netlist
from rich.console import Console


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="kle2netlist",
    help="KiCad netlist generator for mechanical keyboards ",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]kle2netlist[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="")
def main(
    layout: str = typer.Option(..., help="Path to kle layout file"),
    output: str = typer.Option(..., help="Path to output"),
    color: Optional[Color] = typer.Option(
        None,
        "-c",
        "--color",
        "--colour",
        case_sensitive=False,
        help="Color for name. If not specified then choice will be random.",
    ),
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the kle2netlist package.",
    ),
):
    """Prints a greeting for a giving name."""
    if color is None:
        # If no color specified use random value from `Color` class
        color = random.choice(list(Color.__members__.values()))

    console.print(f"[bold {color}]{layout}[/]")

    with open(layout) as f:
        json_layout = json.loads(f.read())
        kle2netlist(json_layout, output)

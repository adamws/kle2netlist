# type: ignore[attr-defined]

from typing import List, Optional

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
    switch_library: str = typer.Option(
        "perigoso/Switch_Keyboard", "-swl", "--switch-library", help="todo"
    ),
    switch_footprint: str = typer.Option(
        "MX", "-swf", "--switch-footprint", help="todo"
    ),
    lib_paths: Optional[List[str]] = typer.Option(
        None, "-l", "--lib-path", help="Path to symbol library"
    ),
    controller_circuit: bool = typer.Option(
        False,
        "--controller-circuit",
        help="Add ATmega32U4-AU minimal circuitry",
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
    """Generates KiCad netlist for a given keyboard layout json file."""

    with open(layout) as f:
        json_layout = json.loads(f.read())
        kle2netlist(
            json_layout,
            output,
            switch_library=switch_library,
            switch_footprint=switch_footprint,
            additional_search_path=lib_paths,
            controller_circuit=controller_circuit,
        )

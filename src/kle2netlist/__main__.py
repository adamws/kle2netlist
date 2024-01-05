# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import json
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from kle2netlist._version import __version__
from kle2netlist.skidl import build_circuit, generate_netlist


class SwitchType(str, Enum):
    mx = "MX"
    alps = "Alps"
    mx_alps_hybrid = "MX/Alps Hybrid"


app = typer.Typer(
    name="kle2netlist",
    help="KiCad netlist generator for mechanical keyboards ",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(f"[yellow]kle2netlist[/] version: [bold blue]{__version__}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    layout: Path = typer.Option(..., help="Path to kle layout file"),
    output: Path = typer.Option(
        ".", "--output-dir", help="Output directory, created if not existing"
    ),
    name: str = typer.Option(
        "keyboard", "--name", help="Netlist name without file extension"
    ),
    switch_library: str = typer.Option(
        "kiswitch/keyswitch-kicad-library",
        "-swl",
        "--switch-library",
        help="Switch library",
    ),
    switch_footprint: SwitchType = typer.Option(
        SwitchType.mx, "-swf", "--switch-footprint", help="Switch footprint"
    ),
    diode_footprint: str = typer.Option(
        "D_SOD-323F", "-df", "--diode-footprint", help="Diode footprint"
    ),
    lib_paths: Optional[List[str]] = typer.Option(
        None, "-l", "--lib-path", help="Path to symbol library"
    ),
    controller_circuit: bool = typer.Option(
        False,
        "--controller-circuit",
        help="Add ATmega32U4-AU minimal circuitry",
    ),
    no_xml: bool = typer.Option(False, "--no-xml", help="Skip xml netlist generation"),
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

    if output.is_file():
        console.print(
            f"[red]error:[/] --output-directory pointing to an existing file: [bold]{output}[/]"
        )
        raise typer.Exit(code=1)

    output.mkdir(exist_ok=True, parents=True)

    if not Path(layout).is_file():
        console.print(
            f"[red]error:[/] invalid --layout option: [bold]{layout}[/] file not found"
        )
        raise typer.Exit(code=1)

    try:
        with open(layout) as f:
            json_layout = json.loads(f.read())
            build_circuit(
                json_layout,
                switch_library=switch_library,
                switch_footprint=switch_footprint,
                diode_footprint=diode_footprint,
                additional_search_path=lib_paths,
                controller_circuit=controller_circuit,
            )

        generate_netlist(str(output.joinpath(f"{name}.net")))
        if not no_xml:
            generate_netlist(str(output.joinpath(f"{name}.xml")), "xml")
    except RuntimeError as e:
        console.print(f"[red]error:[/] [bold]{e}[/]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

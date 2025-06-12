# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

from kle2netlist._version import __version__
from kle2netlist.keyboard import load_keyboard
from kle2netlist.netlist import build_circuit, generate_netlist, generate_pcb
from kle2netlist.utilities import get_circuit_revision

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
    netlist_output: Path = typer.Option(
        "keyboard.net", "--netlist-output", help="Output netlist file"
    ),
    switch_footprint: str = typer.Option(
        "PCM_Switch_Keyboard_Cherry_MX:SW_Cherry_MX_PCB_{:.2f}u",
        "-swf",
        "--switch-footprint",
        help="Switch footprint f-string",
    ),
    stabilizer_footprint: str = typer.Option(
        "PCM_Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{:.2f}u",
        "-stf",
        "--stabilizer-footprint",
        help="Stabilizer footprint f-string, optional",
    ),
    diode_footprint: str = typer.Option(
        "Diode_SMD:D_SOD-123F", "-df", "--diode-footprint", help="Diode footprint"
    ),
    # use this feature https://github.com/fastapi/typer/pull/800 when merged:
    lib_paths: Optional[str] = typer.Option(
        None, "-l", "--lib-path", help="Path to symbol library"
    ),
    controller_circuit: Optional[str] = typer.Option(
        None,
        "--controller-circuit",
        help="Name of controller circuit",
    ),
    extra_circuits: Optional[List[str]] = typer.Option(
        None,
        "--extra-circuits",
        help="Extra circuits",
    ),
    # use this feature https://github.com/fastapi/typer/pull/800 when merged:
    row_column_pin_order: Optional[str] = typer.Option(
        None,
        "--row-column-pin-order",
        help="Comma separated list of microcontroller pins defining order of row/column assignments",
    ),
    pcb_output: Optional[Path] = typer.Option(
        None, "--pcb-output", help="Output kicad_pcb file"
    ),
    force: bool = typer.Option(False, "--force", help="Override output files"),
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

    if not force:
        if netlist_output.is_file():
            console.print(
                f"[red]error:[/] --netlist-output pointing to an existing file: [bold]{netlist_output}[/]"
            )
            raise typer.Exit(code=1)
        if pcb_output and pcb_output.is_file():
            console.print(
                f"[red]error:[/] --pcb-output pointing to an existing file: [bold]{pcb_output}[/]"
            )
            raise typer.Exit(code=1)

    if not Path(layout).is_file():
        console.print(
            f"[red]error:[/] invalid --layout option: [bold]{layout}[/] file not found"
        )
        raise typer.Exit(code=1)

    try:
        keyboard = load_keyboard(layout)
        circuit = build_circuit(
            keyboard=keyboard,
            switch_footprint=switch_footprint,
            stabilizer_footprint=stabilizer_footprint,
            diode_footprint=diode_footprint,
            controller_circuit=controller_circuit,
            extra_circuits=extra_circuits,
            additional_search_path=lib_paths.split(",") if lib_paths else None,
            row_column_pin_order=(
                row_column_pin_order.split(",") if row_column_pin_order else None
            ),
        )

        generate_netlist(circuit, netlist_output)

        if pcb_output:
            from kle2netlist.pcb_kicad import apply_template

            generate_pcb(circuit, pcb_output)

            if controller_circuit:
                template, revision, offset = get_circuit_revision(controller_circuit)
                apply_template(pcb_output, template, revision, offset=offset)

            if extra_circuits:
                for extra_circuit in extra_circuits:
                    template, revision, offset = get_circuit_revision(extra_circuit)
                    apply_template(pcb_output, template, revision, offset=offset)

    except RuntimeError as e:
        console.print(f"[red]error:[/] [bold]{e}[/]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

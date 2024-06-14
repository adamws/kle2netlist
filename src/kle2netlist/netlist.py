# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

import skidl

from kle2netlist.circuits import ControllerCircuit
from kle2netlist.keyboard import handle_switch_matrix, load_keyboard
from kle2netlist.skidl import set_skidl_search_path


def build_circuit(
    layout: Union[str, Path],
    switch_footprint: str,
    stabilizer_footprint: str,
    diode_footprint: str,
    controller_circuit: ControllerCircuit = ControllerCircuit.NONE,
    additional_search_path: Optional[List[str]] = None,
) -> skidl.Circuit:
    set_skidl_search_path(additional_search_path)

    circuit = skidl.Circuit()
    with circuit:
        keyboard = load_keyboard(layout)
        rows, columns = handle_switch_matrix(
            keyboard, switch_footprint, diode_footprint, stabilizer_footprint
        )
        controller_circuit.add(rows, columns)
    return circuit


def generate_netlist(circuit: skidl.Circuit, output: Union[str, Path]) -> None:
    circuit.generate_netlist(file_=str(output))


__all__ = ["build_circuit", "generate_netlist"]

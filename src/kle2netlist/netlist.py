# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

import skidl

from kle2netlist.circuits import get_circuit
from kle2netlist.keyboard import handle_switch_matrix, load_keyboard
from kle2netlist.skidl import set_skidl_search_path


def __connect_interfaces(interfaces: List[skidl.Interface]) -> None:
    all_keys = set().union(*interfaces)
    values_by_key = {key: [d.get(key, None) for d in interfaces] for key in all_keys}
    for k, v in values_by_key.items():
        for p1, p2 in zip(v, v[1:]):
            if p1 and p2:
                p1 += p2


def build_circuit(
    layout: Union[str, Path],
    switch_footprint: str,
    stabilizer_footprint: str,
    diode_footprint: str,
    controller_circuit: Optional[str] = None,
    extra_circuits: Optional[List[str]] = None,
    row_column_pin_order: Optional[List[str]] = None,
    additional_search_path: Optional[List[str]] = None,
) -> skidl.Circuit:
    set_skidl_search_path(additional_search_path)

    circuit = skidl.Circuit()
    with circuit:
        interfaces = []

        keyboard = load_keyboard(layout)
        matrix_interface = handle_switch_matrix(
            keyboard, switch_footprint, diode_footprint, stabilizer_footprint
        )
        interfaces.append(matrix_interface)

        if controller_circuit:
            controller = get_circuit(controller_circuit)
            ret = controller.add("v1", matrix_interface, row_column_pin_order)
            interfaces.append(ret)

        if extra_circuits:
            for circuit_name in extra_circuits:
                subcircuit = get_circuit(circuit_name)
                ret = subcircuit.add("v1")
                interfaces.append(ret)

        __connect_interfaces(interfaces)
        circuit.merge_net_names()

    return circuit


def generate_netlist(circuit: skidl.Circuit, output: Union[str, Path]) -> None:
    circuit.generate_netlist(file_=str(output))


__all__ = ["build_circuit", "generate_netlist"]

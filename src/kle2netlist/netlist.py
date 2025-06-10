# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import itertools
import re
from pathlib import Path
from typing import List, Optional, Union

import skidl
from kbplacer.kle_serial import MatrixAnnotatedKeyboard

from kle2netlist.circuits import get_circuit_revision
from kle2netlist.keyboard import handle_switch_matrix
from kle2netlist.skidl import set_skidl_search_path


def __connect_interfaces(interfaces: List[skidl.Interface]) -> None:
    all_keys = set().union(*interfaces)
    values_by_key = {key: [d.get(key, None) for d in interfaces] for key in all_keys}
    for k, v in values_by_key.items():
        for p1, p2 in zip(v, v[1:]):
            if p1 and p2:
                p1 += p2


def __split_dict(matrix_interface):
    rows = {}
    columns = {}
    for key, value in matrix_interface.items():
        if re.fullmatch(r"ROW\d+", key):
            rows[key] = value
        elif re.fullmatch(r"COL\d+", key):
            columns[key] = value

    return rows, columns


def __split_controller_interface(
    controller_interface: skidl.Interface, matrix_interface: Optional[skidl.Interface]
) -> skidl.Interface:
    controller_mapping = {}
    i = 0

    if matrix_interface:
        rows, columns = __split_dict(matrix_interface)

        for key in itertools.chain(sorted(rows), sorted(columns)):
            pin = controller_interface.pop(f"io{i}", None)
            if not pin:
                msg = "Controller circuit with can't handle requested matrix"
                raise RuntimeError(msg)

            controller_mapping[key] = pin
            i += 1

    return skidl.Interface(controller_mapping)


def __remove_unused_io_from_controller_interface(
    controller_interface: skidl.Interface, circuit: skidl.Circuit
) -> None:
    # remove any remaining IO from controller_interface
    # if there is more than needed for matrix_interface
    for k in list(controller_interface):
        if k.startswith("io"):
            net = controller_interface.pop(k, None)
            # must disconnect all pins first, otherwise rmv_stuff won't work
            for pin in net.get_pins():
                net.disconnect(pin)
                pin.disconnect()
            circuit.rmv_stuff(net)


def build_circuit(
    *,
    keyboard: Optional[MatrixAnnotatedKeyboard] = None,
    switch_footprint: str = "",
    stabilizer_footprint: str = "",
    diode_footprint: str = "",
    controller_circuit: Optional[str] = None,
    extra_circuits: Optional[List[str]] = None,
    row_column_pin_order: Optional[List[str]] = None,
    additional_search_path: Optional[List[str]] = None,
) -> skidl.Circuit:
    set_skidl_search_path(additional_search_path)

    circuit = skidl.Circuit()
    with circuit:
        interfaces = []

        matrix_interface = None
        if keyboard:
            matrix_interface = handle_switch_matrix(
                keyboard, switch_footprint, diode_footprint, stabilizer_footprint
            )
            interfaces.append(matrix_interface)

        if controller_circuit:
            controller, revision = get_circuit_revision(controller_circuit)
            controller_interface = controller.add(revision, row_column_pin_order)
            if keyboard:
                # if keyboard has been added, pop all io's from controller
                # interface and create new matching interface with ROWs/COLs and controller pins
                controller_matrix_interface = __split_controller_interface(
                    controller_interface, matrix_interface
                )
                interfaces.append(controller_matrix_interface)
                __remove_unused_io_from_controller_interface(
                    controller_interface, circuit
                )

            interfaces.append(controller_interface)

        if extra_circuits:
            for extra_circuit in extra_circuits:
                subcircuit, revision = get_circuit_revision(extra_circuit)
                extra_interface = subcircuit.add(revision)
                interfaces.append(extra_interface)

        __connect_interfaces(interfaces)
        circuit.merge_net_names()

    return circuit


def generate_netlist(circuit: skidl.Circuit, output: Union[str, Path]) -> None:
    circuit.generate_netlist(file_=str(output))


def generate_pcb(circuit: skidl.Circuit, output: Union[str, Path]) -> None:
    libraries = ["/usr/share/kicad/footprints"]
    circuit.generate_pcb(file_=output, fp_libs=libraries)


__all__ = ["build_circuit", "generate_netlist", "generate_pcb"]

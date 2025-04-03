# SPDX-FileCopyrightText: 2025-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import argparse

import pcbnew
import skidl

from kle2netlist.circuits import get_circuit
from kle2netlist.pcb import (
    add_tracks,
    add_vias,
    set_positions,
    Footprint,
    Track,
    Via,
)
from kle2netlist.skidl import set_skidl_search_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate kicad_pcb templates")
    parser.add_argument(
        "--circuit",
        required=True,
        choices=["atmega32u4", "usb"],
        help="Choose circuit",
    )
    parser.add_argument(
        "--rev",
        required=True,
        help="Choose circuit revision",
    )

    args = parser.parse_args()
    circuit_name = args.circuit
    rev = args.rev
    circuit = get_circuit(circuit_name)

    set_skidl_search_path()

    board_path = f"{circuit_name}_{rev}.kicad_pcb"

    _circuit = skidl.Circuit()
    with _circuit:
        if circuit.matrix_pins():
            rows = skidl.Interface()
            for i in range(0, len(circuit.matrix_pins())):
                # fake rows in order to plot fanout tracks
                rows[f"ROW{i}"] = skidl.Net(f"io{i}", fixed_name=True)
            circuit.add(rev, rows)
        else:
            circuit.add(rev)

    libraries = ["/usr/share/kicad/footprints"]
    _circuit.generate_pcb(file_=board_path, fp_libs=libraries)

    board = pcbnew.LoadBoard(board_path)

    footprints = [Footprint.fromdict_mm(d) for d in circuit.positions(rev)]
    set_positions(board, footprints)

    tracks = [Track.fromdict_mm(d) for d in circuit.tracks(rev)]
    add_tracks(board, tracks)

    for pin in circuit.matrix_pins():
        fanout_tracks = circuit.fanout_tracks(rev)
        if tracks := fanout_tracks.get(pin, None):
            fanout_tracks = [Track.fromdict_mm(d) for d in tracks]
            add_tracks(board, fanout_tracks)

    vias = [Via.fromdict_mm(d) for d in circuit.vias(rev)]
    add_vias(board, vias)

    pcbnew.SaveBoard(board_path, board)

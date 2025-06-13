# SPDX-FileCopyrightText: 2025-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import asdict
from types import ModuleType
from typing import Dict, List, Optional, Tuple, Union

import pcbnew
from kbplacer.board_modifier import (
    get_footprint,
    get_orientation,
    get_side,
    rotate,
    set_position,
    set_rotation,
    set_side,
)
from kbplacer.element_position import Side

from kle2netlist.pcb import Footprint, Track, Via, mm_to_nm, normalize

version_match = re.search(r"(\d+)\.(\d+)\.(\d+)", pcbnew.Version())
KICAD_VERSION = tuple(map(int, version_match.groups())) if version_match else ()
MIN_KICAD_VERSION = (8, 0, 0)

if KICAD_VERSION < MIN_KICAD_VERSION:
    raise RuntimeError("Unsupported KiCad version")


def get_positions(
    board: pcbnew.BOARD, *, ignore_pattern: Optional[re.Pattern] = None
) -> List[Footprint]:
    positions = []
    for fp in board.GetFootprints():
        ref_str = fp.GetReference()
        if ignore_pattern and re.match(ignore_pattern, ref_str):
            continue

        reference = fp.Reference()
        reference_position = reference.GetFPRelativePosition()

        position = Footprint(
            ref=ref_str,
            x=fp.GetX(),
            y=fp.GetY(),
            rotation=get_orientation(fp),
            side=get_side(fp),
            ref_x=reference_position.x,
            ref_y=reference_position.y,
        )
        positions.append(position)

    return sorted(positions, key=lambda x: x.ref)


def set_positions(
    board: pcbnew.BOARD,
    footprints: List[Footprint],
    *,
    offset: pcbnew.VECTOR2I = pcbnew.VECTOR2I(0, 0),
    angle: float = 0,
) -> None:
    for f in footprints:
        if fp := board.FindFootprintByReference(f.ref):
            set_side(fp, Side(f.side))
            set_rotation(fp, f.rotation)
            set_position(fp, pcbnew.VECTOR2I(f.x, f.y) + offset)
            reference = fp.Reference()
            reference.SetFPRelativePosition(pcbnew.VECTOR2I(f.ref_x, f.ref_y))
            rotate(fp, offset, angle)


def get_tracks(board: pcbnew.BOARD) -> List[Track]:
    tracks = []
    for t in board.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            continue
        # ignore tracks of f'io{i}' nets (those will be stored in separate collection)
        if t.GetNetname().startswith("io"):
            continue
        start = t.GetStart()
        end = t.GetEnd()
        width = t.GetWidth()
        track = Track(
            x1=start.x,
            y1=start.y,
            x2=end.x,
            y2=end.y,
            width=width,
            layer=t.GetLayerName(),
        )
        tracks.append(track)
    tracks.sort()
    return tracks


def get_tracks_by_net(
    board: pcbnew.BOARD, *, name_prefix: str = ""
) -> Dict[str, List[Track]]:
    tracks: Dict[str, List[Track]] = defaultdict(list)
    for t in board.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            continue
        netname = t.GetNetname()
        if name_prefix == "" or netname.startswith(name_prefix):
            start = t.GetStart()
            end = t.GetEnd()
            width = t.GetWidth()
            track = Track(
                x1=start.x,
                y1=start.y,
                x2=end.x,
                y2=end.y,
                width=width,
                layer=t.GetLayerName(),
            )
            tracks[netname].append(track)
    for v in tracks.values():
        v.sort()
    return tracks


def add_tracks(
    board: pcbnew.BOARD,
    tracks: List[Track],
    *,
    offset: pcbnew.VECTOR2I = pcbnew.VECTOR2I(0, 0),
    angle: float = 0,
) -> None:
    for t in tracks:
        track = pcbnew.PCB_TRACK(board)
        track.SetWidth(t.width)
        track.SetLayer(board.GetLayerID(t.layer))
        track.SetStart(pcbnew.VECTOR2I(t.x1, t.y1) + offset)
        track.SetEnd(pcbnew.VECTOR2I(t.x2, t.y2) + offset)
        rotate(track, offset, angle)
        board.Add(track)


def get_vias(board: pcbnew.BOARD) -> List[Via]:
    vias = []
    for t in board.GetTracks():
        if t.Type() != pcbnew.PCB_VIA_T:
            continue
        via = pcbnew.Cast_to_PCB_VIA(t)
        start = via.GetStart()
        via_serialized = Via(
            x=start.x,
            y=start.y,
            width=via.GetWidth(),
            hole=via.GetDrill(),
        )
        vias.append(via_serialized)
    vias.sort()
    return vias


def add_vias(
    board: pcbnew.BOARD,
    vias: List[Via],
    *,
    offset: pcbnew.VECTOR2I = pcbnew.VECTOR2I(0, 0),
    angle: float = 0,
) -> None:
    for v in vias:
        via = pcbnew.PCB_VIA(board)
        via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetStart(pcbnew.VECTOR2I(v.x, v.y) + offset)
        via.SetDrill(v.hole)
        via.SetTopLayer(pcbnew.F_Cu)
        via.SetBottomLayer(pcbnew.B_Cu)
        if KICAD_VERSION < (9, 0, 0):
            via.SetWidth(v.width)
        else:
            for layer in [pcbnew.F_Cu, pcbnew.B_Cu]:
                via.SetWidth(layer, v.width)
        rotate(via, offset, angle)
        board.Add(via)


def apply_template(
    board_path: str,
    template: ModuleType,
    template_rev: str,
    *,
    offset: Union[Tuple[float, float], Tuple[str, str]] = (0, 0),
    angle: float = 0,
) -> None:
    board = pcbnew.LoadBoard(board_path)

    offset = pcbnew.VECTOR2I(mm_to_nm(offset[0]), mm_to_nm(offset[1]))

    footprints = [Footprint.fromdict_mm(d) for d in template.positions(template_rev)]
    set_positions(board, footprints, offset=offset, angle=angle)

    tracks = [Track.fromdict_mm(d) for d in template.tracks(template_rev)]
    add_tracks(board, tracks, offset=offset, angle=angle)

    # works only for controller circuits which have matrix_pins defined
    # but could be generalized.
    fanout_tracks = template.fanout_tracks(template_rev)
    for item, tracks in fanout_tracks.items():
        f = get_footprint(board, item)
        for pin_name, pin_number in template.matrix_pins():
            pad = f.FindPadByNumber(f"{pin_number}")
            if pad.GetNetname():
                if tracks_for_pin := tracks.get(pin_name, None):
                    fanout_tracks = [Track.fromdict_mm(d) for d in tracks_for_pin]
                    add_tracks(board, fanout_tracks, offset=offset, angle=angle)

    vias = [Via.fromdict_mm(d) for d in template.vias(template_rev)]
    add_vias(board, vias, offset=offset, angle=angle)

    pcbnew.SaveBoard(board_path, board)


def _get_board_path(source: str) -> Tuple[bool, str]:
    if source.startswith("http"):
        response = requests.get(source)
        assert response.status_code == 200, f"Download from {source} failed"

        pcb_file = tempfile.NamedTemporaryFile(delete=False, suffix=".kicad_pcb")
        pcb_file.write(response.content)
        pcb_file.close()
        return True, str(pcb_file.name)
    return False, source


if __name__ == "__main__":
    import argparse
    import os
    import tempfile

    import requests

    parser = argparse.ArgumentParser(description="Process PCB")
    parser.add_argument(
        "--action",
        required=True,
        default="positions",
        choices=["positions", "tracks", "io_tracks", "vias"],
    )
    parser.add_argument("board", type=str, help="Filepath or URL")

    args = parser.parse_args()
    action = args.action

    remove_later, pcb_file_path = _get_board_path(str(args.board))
    board = pcbnew.LoadBoard(pcb_file_path)

    if action == "positions":
        ignore_pattern = re.compile("(K.*)|(D.*)")

        positions = get_positions(board, ignore_pattern=ignore_pattern)

        normalize(positions, "U1")

        json_encoded = json.dumps(positions, default=lambda x: asdict(x))
        json_decoded = json.loads(json_encoded)
        for f in json_decoded:
            f = Footprint.fromdict(f)
            f.pprint(to_mm=True)

        footprints = [Footprint.fromdict(d) for d in json_decoded]
        set_positions(board, footprints)
    elif action == "tracks":
        tracks = get_tracks(board)
        for t in tracks:
            t.pprint(to_mm=True)
    elif action == "io_tracks":
        tracks = get_tracks_by_net(board, name_prefix="io")
        for net, tracks in tracks.items():
            # must convert these to pin names when copying to circuit data:
            print(f"{net}:")
            for t in tracks:
                t.pprint(to_mm=True)
    elif action == "vias":
        vias = get_vias(board)
        for v in vias:
            v.pprint(to_mm=True)

    if remove_later:
        os.remove(pcb_file_path)

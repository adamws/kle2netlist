from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass, fields
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Dict, List, Optional, Tuple

import pcbnew
from kbplacer.board_modifier import (
    get_orientation,
    get_side,
    set_position,
    set_rotation,
    set_side,
)
from kbplacer.element_position import Side

version_match = re.search(r"(\d+)\.(\d+)\.(\d+)", pcbnew.Version())
KICAD_VERSION = tuple(map(int, version_match.groups())) if version_match else ()
MIN_KICAD_VERSION = (8, 0, 0)

if KICAD_VERSION < MIN_KICAD_VERSION:
    raise RuntimeError("Unsupported KiCad version")


def mm_to_nm(mm_str: str) -> int:
    mm = Decimal(mm_str)
    nm = mm * Decimal("1000000")
    nm = nm.quantize(Decimal("1"), rounding=ROUND_HALF_EVEN)
    return int(nm)


def nm_to_mm(nm: int) -> str:
    mm = Decimal(nm) / Decimal("1000000")
    mm = mm.quantize(Decimal("0.00001"), rounding=ROUND_HALF_EVEN).normalize()
    return f"{mm:.1f}" if mm == mm.to_integral() else str(mm)


@dataclass
class Footprint:
    ref: str
    x: int
    y: int
    rotation: float
    side: Side
    ref_x: int
    ref_y: int

    POS_FIELDS = ["x", "y", "ref_x", "ref_y"]

    @classmethod
    def fromdict(cls, data: dict):
        return cls(**data)

    @classmethod
    def fromdict_mm(cls, data: dict):
        for field in data:
            if field in cls.POS_FIELDS:
                data[field] = mm_to_nm(data[field])
        return cls(**data)

    def pprint(self, to_mm=False) -> None:
        formats = [">8", ">10", ">10", "6", ">7", ">9", ">9"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
            if to_mm and isinstance(value, int):
                value = nm_to_mm(value)
            format_string = f'"{f.name}": {value:{x}}'
            items.append(format_string)
        print("{ " + ", ".join(items) + " },")


@dataclass(order=True)
class Track:
    x1: int
    y1: int
    x2: int
    y2: int
    width: int
    layer: str

    POS_FIELDS = ["x1", "y1", "x2", "y2", "width"]

    @classmethod
    def fromdict(cls, data: dict):
        return cls(**data)

    @classmethod
    def fromdict_mm(cls, data: dict):
        for field in data:
            if field in cls.POS_FIELDS:
                data[field] = mm_to_nm(data[field])
        return cls(**data)

    def pprint(self, to_mm=False) -> None:
        formats = [">10", ">10", ">10", ">10", ">10", ">6"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
            if to_mm and isinstance(value, int):
                value = nm_to_mm(value)
            format_string = f'"{f.name}": {value:{x}}'
            items.append(format_string)
        print("{ " + ", ".join(items) + " },")


@dataclass(order=True)
class Via:
    x: int
    y: int
    width: int
    hole: int

    POS_FIELDS = ["x", "y", "width", "hole"]

    @classmethod
    def fromdict(cls, data: dict):
        return cls(**data)

    @classmethod
    def fromdict_mm(cls, data: dict):
        for field in data:
            data[field] = mm_to_nm(data[field])
        return cls(**data)

    def pprint(self, to_mm=False) -> None:
        formats = [">10", ">10", ">10", ">10"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
            if to_mm and isinstance(value, int):
                value = nm_to_mm(value)
            format_string = f'"{f.name}": {value:{x}}'
            items.append(format_string)
        print("{ " + ", ".join(items) + " },")


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


def normalize(footprints: List[Footprint], reference: str) -> None:
    reference_fp = list(filter(lambda x: x.ref == reference, footprints))
    assert len(reference_fp) == 1
    origin_x, origin_y = reference_fp[0].x, reference_fp[0].y
    for fp in footprints:
        fp.x = fp.x - origin_x
        fp.y = fp.y - origin_y


def set_positions(
    board: pcbnew.BOARD,
    footprints: List[Footprint],
    *,
    offset: pcbnew.VECTOR2I = pcbnew.VECTOR2I(0, 0),
) -> None:
    for f in footprints:
        if fp := board.FindFootprintByReference(f.ref):
            set_side(fp, f.side)
            set_rotation(fp, f.rotation)
            set_position(fp, pcbnew.VECTOR2I(f.x, f.y) + offset)
            reference = fp.Reference()
            reference.SetFPRelativePosition(pcbnew.VECTOR2I(f.ref_x, f.ref_y))


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
) -> None:
    for t in tracks:
        track = pcbnew.PCB_TRACK(board)
        track.SetWidth(t.width)
        track.SetLayer(board.GetLayerID(t.layer))
        track.SetStart(pcbnew.VECTOR2I(t.x1, t.y1) + offset)
        track.SetEnd(pcbnew.VECTOR2I(t.x2, t.y2) + offset)
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
        board.Add(via)


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

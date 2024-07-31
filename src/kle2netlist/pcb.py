from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, fields
from typing import List, Optional, Tuple, Type

import pcbnew
from kbplacer.board_modifier import (
    get_orientation,
    get_side,
    set_position,
    set_rotation,
    set_side,
)
from kbplacer.element_position import Side


@dataclass
class Footprint:
    ref: str
    x: float
    y: float
    rotation: float
    side: Side
    ref_x: float
    ref_y: float

    @classmethod
    def fromdict(cls: Type[Footprint], data: dict) -> Footprint:
        return cls(**data)

    def pprint(self) -> None:
        formats = [">8", "10", "10", "6", ">7", "9", "9"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
            format_string = f'"{f.name}": {value:{x}}'
            items.append(format_string)
        print("{ " + ", ".join(items) + " },")


@dataclass(order=True)
class Track:
    x1: float
    y1: float
    x2: float
    y2: float
    width: float
    layer: int

    @classmethod
    def fromdict(cls: Type[Track], data: dict) -> Track:
        return cls(**data)

    def pprint(self) -> None:
        formats = ["10", "10", "10", "10", "5", "2"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
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
            x=pcbnew.ToMM(fp.GetX()),
            y=pcbnew.ToMM(fp.GetY()),
            rotation=get_orientation(fp),
            side=get_side(fp),
            ref_x=pcbnew.ToMM(reference_position.x),
            ref_y=pcbnew.ToMM(reference_position.y),
        )
        positions.append(position)

    return sorted(positions, key=lambda x: x.ref)


def normalize(footprints: List[Footprint], reference: str) -> None:
    reference_fp = list(filter(lambda x: x.ref == reference, footprints))
    assert len(reference_fp) == 1
    origin_x, origin_y = reference_fp[0].x, reference_fp[0].y
    for fp in footprints:
        fp.x = round(fp.x - origin_x, 6)
        fp.y = round(fp.y - origin_y, 6)


def set_positions(board: pcbnew.BOARD, footprints: List[Footprint]) -> None:
    for f in footprints:
        if fp := board.FindFootprintByReference(f.ref):
            set_side(fp, f.side)
            set_rotation(fp, f.rotation)
            set_position(fp, pcbnew.VECTOR2I_MM(f.x, f.y))
            reference = fp.Reference()
            reference.SetFPRelativePosition(pcbnew.VECTOR2I_MM(f.ref_x, f.ref_y))


def get_tracks(board: pcbnew.BOARD) -> List[Track]:
    tracks = []
    for t in board.GetTracks():
        start = t.GetStart()
        end = t.GetEnd()
        width = t.GetWidth()
        track = Track(
            x1=pcbnew.ToMM(start.x),
            y1=pcbnew.ToMM(start.y),
            x2=pcbnew.ToMM(end.x),
            y2=pcbnew.ToMM(end.y),
            width=pcbnew.ToMM(width),
            layer=t.GetLayer(),
        )
        tracks.append(track)
    tracks.sort()
    return tracks


def add_tracks(board: pcbnew.BOARD, tracks: List[Track]) -> None:
    for t in tracks:
        track = pcbnew.PCB_TRACK(board)
        track.SetWidth(pcbnew.FromMM(t.width))
        track.SetLayer(t.layer)
        track.SetStart(pcbnew.VECTOR2I_MM(t.x1, t.y1))
        track.SetEnd(pcbnew.VECTOR2I_MM(t.x2, t.y2))
        board.Add(track)


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
        "--action", required=True, default="positions", choices=["positions", "tracks"]
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
            f.pprint()

        positions = [Footprint.fromdict(d) for d in json_decoded]
        set_positions(board, positions)
    elif action == "tracks":
        tracks = get_tracks(board)
        for t in tracks:
            t.pprint()

    if remove_later:
        os.remove(pcb_file_path)

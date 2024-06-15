from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pprint import pprint
from typing import List, Type

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

    @classmethod
    def fromdict(cls: Type[Footprint], data: dict) -> Footprint:
        return cls(**data)


def get_positions(board: pcbnew.BOARD) -> List[Footprint]:
    positions = []
    for fp in board.GetFootprints():
        position = Footprint(
            ref=fp.GetReference(),
            x=pcbnew.ToMM(fp.GetX()),
            y=pcbnew.ToMM(fp.GetY()),
            rotation=get_orientation(fp),
            side=get_side(fp),
        )
        positions.append(position)

    return sorted(positions, key=lambda x: x.ref)


def set_positions(board: pcbnew.BOARD, footprints: List[Footprint]) -> None:
    for f in footprints:
        fp = board.FindFootprintByReference(f.ref)
        set_side(fp, f.side)
        set_rotation(fp, f.rotation)
        set_position(fp, pcbnew.wxPointMM(f.x, f.y))


if __name__ == "__main__":
    pcb_file = "./kicad-templates/atmega32u4-au-v1/atmega32u4-au-v1.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_file)
    positions = get_positions(board)
    json_encoded = json.dumps(positions, default=lambda x: asdict(x))

    json_decoded = json.loads(json_encoded)
    pprint(json_decoded)

    positions = [Footprint.fromdict(d) for d in json_decoded]
    set_positions(board, positions)

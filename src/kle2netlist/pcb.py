from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
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
    ref_x: float
    ref_y: float

    @classmethod
    def fromdict(cls: Type[Footprint], data: dict) -> Footprint:
        return cls(**data)

    def pprint(self) -> None:
        formats = [">6", "5", "7", "6", "4", "9", "9"]
        items = []
        for f, x in zip(fields(self), formats):
            value = getattr(self, f.name)
            if isinstance(value, str):
                value = '"' + value + '"'
            format_string = f'"{f.name}": {value:{x}}'
            items.append(format_string)
        print("{ " + ", ".join(items) + " },")


def get_positions(board: pcbnew.BOARD) -> List[Footprint]:
    positions = []
    for fp in board.GetFootprints():
        reference = fp.Reference()
        reference_position = reference.GetFPRelativePosition()

        position = Footprint(
            ref=fp.GetReference(),
            x=pcbnew.ToMM(fp.GetX()),
            y=pcbnew.ToMM(fp.GetY()),
            rotation=get_orientation(fp),
            side=get_side(fp),
            ref_x=pcbnew.ToMM(reference_position.x),
            ref_y=pcbnew.ToMM(reference_position.y),
        )
        positions.append(position)

    return sorted(positions, key=lambda x: x.ref)


def set_positions(board: pcbnew.BOARD, footprints: List[Footprint]) -> None:
    for f in footprints:
        fp = board.FindFootprintByReference(f.ref)
        set_side(fp, f.side)
        set_rotation(fp, f.rotation)
        set_position(fp, pcbnew.wxPointMM(f.x, f.y))
        reference = fp.Reference()
        reference.SetFPRelativePosition(pcbnew.VECTOR2I_MM(f.ref_x, f.ref_y))


if __name__ == "__main__":
    pcb_file = "./kicad-templates/atmega32u4-au-v1/atmega32u4-au-v1.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_file)
    positions = get_positions(board)
    json_encoded = json.dumps(positions, default=lambda x: asdict(x))

    json_decoded = json.loads(json_encoded)
    for f in json_decoded:
        f = Footprint.fromdict(f)
        f.pprint()

    positions = [Footprint.fromdict(d) for d in json_decoded]
    set_positions(board, positions)

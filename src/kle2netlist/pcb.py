from __future__ import annotations

import json
from typing import Dict, Union

import pcbnew
from kbplacer.board_modifier import (
    get_orientation,
    get_side,
    set_position,
    set_rotation,
    set_side,
)
from kbplacer.element_position import ElementPosition, Side


class PositionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ElementPosition):
            return {"x": obj.x, "y": obj.y, "rot": obj.orientation, "side": obj.side}
        return super().default(obj)


class PositionDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=PositionDecoder.from_dict)

    @staticmethod
    def from_dict(d):
        if set(d.keys()) == set(["x", "y", "rot", "side"]):
            return PositionDecoder.element_position_from_dict(d)
        return d

    @staticmethod
    def element_position_from_dict(d) -> ElementPosition:
        return ElementPosition(
            d["x"],
            d["y"],
            d["rot"],
            Side.get(d["side"]),
        )


def get_positions(board: pcbnew.BOARD) -> Dict[str, ElementPosition]:
    positions = {}
    for fp in board.GetFootprints():
        reference = fp.GetReference()
        position = ElementPosition(
            x=pcbnew.ToMM(fp.GetX()),
            y=pcbnew.ToMM(fp.GetY()),
            orientation=get_orientation(fp),
            side=get_side(fp),
        )
        positions[reference] = position

    return dict(sorted(positions.items()))


def set_positions(
    board: pcbnew.BOARD, positions: Union[Dict[str, ElementPosition], Dict[str, Dict]]
) -> None:
    for ref, position in positions.items():
        fp = board.FindFootprintByReference(ref)
        if not isinstance(position, ElementPosition):
            position = PositionDecoder.element_position_from_dict(position)
        set_side(fp, position.side)
        set_rotation(fp, position.orientation)
        set_position(fp, pcbnew.wxPointMM(position.x, position.y))


if __name__ == "__main__":
    pcb_file = "./kicad-templates/atmega32u4-au-v1/atmega32u4-au-v1.kicad_pcb"
    board = pcbnew.LoadBoard(pcb_file)
    positions = get_positions(board)
    json_encoded = json.dumps(positions, indent=4, cls=PositionEncoder)
    print(json_encoded)
    json_decoded = json.loads(json_encoded, cls=PositionDecoder)
    set_positions(board, json_decoded)

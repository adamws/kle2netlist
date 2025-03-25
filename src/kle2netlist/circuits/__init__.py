# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, fields
from decimal import Decimal, ROUND_HALF_EVEN
from enum import Enum
from typing import Dict, List, Optional

from kbplacer.element_position import Side
from skidl import Net

from kle2netlist.circuits import atmega32u4

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

    def pprint(self, to_mm = False) -> None:
        formats = [">8", "10", "10", "6", ">7", "9", "9"]
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

    def pprint(self, to_mm = False) -> None:
        formats = [">10", ">10", ">10", ">10", ">5", "2"]
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

    @classmethod
    def fromdict(cls, data: dict):
        return cls(**data)

    @classmethod
    def fromdict_mm(cls, data: dict):
        for field in data:
            data[field] = mm_to_nm(data[field])
        return cls(**data)


class ControllerCircuit(str, Enum):
    NONE = "none"
    ATMEGA32U4_AU_V1 = "atmega32u4_au_v1"

    def add(
        self,
        rows: Dict[str, Net],
        columns: Dict[str, Net],
        row_column_pin_order: Optional[List[str]] = None,
    ) -> None:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            atmega32u4.circuit(
                rows, columns, "v1", row_column_pin_order=row_column_pin_order
            )

    def positions(self) -> List[Footprint]:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            return [Footprint.fromdict_mm(d) for d in atmega32u4.POSITIONS["v1"]]
        else:
            return []

    def tracks(self) -> List[Track]:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            return [Track.fromdict_mm(d) for d in atmega32u4.TRACKS["v1"]]
        else:
            return []

    def tracks_fanout(self, pins: List[str]) -> List[Track]:
        result = []
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            for pin in pins:
                tracks = atmega32u4.TRACKS_FANOUT["v1"].get(pin, None)
                if tracks:
                    result.extend([Track.fromdict_mm(d) for d in tracks])
        return result

    def vias(self) -> List[Via]:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            return [Via.fromdict_mm(d) for d in atmega32u4.VIAS["v1"]]
        else:
            return []

# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass, fields
from enum import Enum
from typing import Dict, List, Optional

from kbplacer.element_position import Side
from skidl import Net

from kle2netlist.circuits import atmega32u4


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
    def fromdict(cls, data: dict):
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
    layer: str

    @classmethod
    def fromdict(cls, data: dict):
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


@dataclass(order=True)
class Via:
    x: float
    y: float

    @classmethod
    def fromdict(cls, data: dict):
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
            return [Footprint.fromdict(d) for d in atmega32u4.POSITIONS["v1"]]
        else:
            return []

    def tracks(self) -> List[Track]:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            return [Track.fromdict(d) for d in atmega32u4.TRACKS["v1"]]
        else:
            return []

    def tracks_fanout(self, pins: List[str]) -> List[Track]:
        result = []
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            for pin in pins:
                tracks = atmega32u4.TRACKS_FANOUT["v1"].get(pin, None)
                if tracks:
                    result.extend([Track.fromdict(d) for d in tracks])
        return result

    def vias(self) -> List[Via]:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            return [Via.fromdict(d) for d in atmega32u4.VIAS["v1"]]
        else:
            return []

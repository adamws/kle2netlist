# SPDX-FileCopyrightText: 2025-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""CAD agnostic representation of PCB elements

This module provides dataclasses for desribing PCB in a way which
does not assume any specific CAD software.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from decimal import ROUND_HALF_EVEN, Decimal
from typing import List, Union


def mm_to_nm(mm: Union[str, float]) -> int:
    nm = Decimal(mm) * Decimal("1000000")
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
    side: str
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


def normalize(footprints: List[Footprint], reference: str) -> None:
    reference_fp = list(filter(lambda x: x.ref == reference, footprints))
    assert len(reference_fp) == 1
    origin_x, origin_y = reference_fp[0].x, reference_fp[0].y
    for fp in footprints:
        fp.x = fp.x - origin_x
        fp.y = fp.y - origin_y

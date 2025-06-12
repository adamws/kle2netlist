# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from types import ModuleType
from typing import Dict, List, Protocol, Tuple

from kle2netlist.circuits import get_circuit


class HasRef(Protocol):
    ref: str


class RefMapper:
    def __init__(self):
        self.mapping: Dict[str, str] = {}

    def add(self, label: str, part: HasRef) -> None:
        self.mapping[label] = part.ref

    def update(self, pairs: Dict[str, HasRef]) -> None:
        for label, part in pairs.items():
            self.mapping[label] = part.ref

    def apply(self, positions: List[Dict]) -> List[Dict]:
        return [{**p, "ref": self.mapping[p["ref"]]} for p in positions]


def get_circuit_revision(name: str) -> Tuple[ModuleType, str, Tuple[str, str]]:
    offset = ("0", "0")
    format_err = (
        "Circuit description must have use following format: "
        "'name,revision[,offset]' where offset is comma delimited "
        "position value: 'x,y'"
    )
    if ";" in name:
        parts = name.split(";")
        if len(parts) not in [2, 3]:
            raise RuntimeError(format_err)
        circuit_name, revision = parts[0], parts[1]
        if len(parts) == 3:
            offset_str = parts[2]
            parts = offset_str.split(",")
            if len(parts) != 2:
                raise RuntimeError(format_err)
            offset = (parts[0], parts[1])
        return get_circuit(circuit_name), revision, offset
    else:
        template = get_circuit(name)
        return template, template.default_revision(), offset

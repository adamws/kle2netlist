# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from enum import Enum

from .atmega32u4 import atmega32u4_au_v1, atmega32u4_au_v2


class ControllerCircuit(str, Enum):
    NONE = "none"
    ATMEGA32U4_AU_V1 = "atmega32u4_au_v1"
    ATMEGA32U4_AU_V2 = "atmega32u4_au_v2"

    def add(self, rows, columns) -> None:
        if self == ControllerCircuit.ATMEGA32U4_AU_V1:
            atmega32u4_au_v1(rows, columns)
        elif self == ControllerCircuit.ATMEGA32U4_AU_V2:
            atmega32u4_au_v2(rows, columns)

# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import bisect
import json
from collections import defaultdict
from pathlib import Path
from typing import Union

import skidl
import yaml
from kbplacer.kle_serial import Key, MatrixAnnotatedKeyboard, get_keyboard


def load_keyboard(layout_path: Union[str, Path]) -> MatrixAnnotatedKeyboard:
    with open(layout_path, encoding="utf-8") as f:
        if str(layout_path).endswith("yaml") or str(layout_path).endswith("yml"):
            layout = yaml.safe_load(f)
        else:
            layout = json.load(f)
        _keyboard = get_keyboard(layout)
        if not isinstance(_keyboard, MatrixAnnotatedKeyboard):
            try:
                _keyboard = MatrixAnnotatedKeyboard(_keyboard.meta, _keyboard.keys)
            except Exception as e:
                msg = (
                    f"Layout from '{layout_path}' is not convertable to "
                    "matrix annotated keyboard which is required for schematic create. "
                    f"Conversion failed with error: '{e}'"
                )
                raise RuntimeError(msg) from e
        _keyboard.collapse()
        return _keyboard


def is_width_supported(key: Key) -> bool:
    # probably should use some searching to see if given footprint exist,
    # for now just assume that any library supports following widths:
    supported_widths = [
        1,
        1.25,
        1.5,
        1.75,
        2,
        2.25,
        2.5,
        2.75,
        3,
        4,
        4.5,
        5.5,
        6,
        6.25,
        6.5,
        7,
    ]
    return key.width in supported_widths


def is_iso_enter(key: Key) -> bool:
    return (
        key.width == 1.25 and key.height == 2 and key.width2 == 1.5 and key.height2 == 1
    )


def find_closest_smaller_or_equal(lst, target):
    index = bisect.bisect_right(lst, target)
    if index == 0:
        return None  # No value is smaller or equal
    else:
        return lst[index - 1]


def add_stabilizer(reference, footprint, key: Key) -> None:
    key_width = max(key.width, key.height)
    supported_stabilizers = [2, 3, 6, 6.25, 7, 8]
    stabilizer_width = find_closest_smaller_or_equal(supported_stabilizers, key_width)

    if stabilizer_width:
        footprint = f"{footprint}".format(stabilizer_width)
        skidl.Part("Mechanical", "MountingHole", footprint=footprint, ref=reference)


def add_regular_switch(reference, footprint, key: Key) -> skidl.Part:
    if not is_width_supported(key) or is_iso_enter(key):
        key_width = 1
    else:
        key_width = key.width

    footprint = footprint.format(key_width)
    return skidl.Part("Switch", "SW_Push", footprint=footprint, ref=reference)


def add_diode(reference, footprint) -> skidl.Part:
    return skidl.Part("Device", "D", footprint=footprint, ref=reference)


def handle_switch_matrix(
    keyboard: MatrixAnnotatedKeyboard,
    switch_footprint,
    diode_footprint,
    stabilizer_footprint,
):
    rows = {}
    columns = {}

    progress: dict[tuple[str, str], list[str]] = defaultdict(list)
    diodes: dict[str, skidl.Part] = {}

    current_ref = 1

    for k in keyboard.keys_in_matrix_order():
        row, column = MatrixAnnotatedKeyboard.get_matrix_position(k)

        row_net = f"ROW{row}" if row.isdigit() else row
        column_net = f"COL{column}" if column.isdigit() else column

        if row not in rows:
            rows[row] = skidl.Net(row_net)
        if column not in columns:
            columns[column] = skidl.Net(column_net)

        position = (row, column)
        layout_option = len(progress[position])
        if layout_option == 0:
            switch_reference = f"SW{current_ref}"
            stab_reference = f"ST{current_ref}"
            diode_reference = f"D{current_ref}"
            current_ref += 1
        else:
            default_switch = progress[position][0]
            default_ref = default_switch[2:]
            switch_reference = f"SW{default_ref}_{layout_option}"
            stab_reference = f"ST{default_ref}_{layout_option}"
            diode_reference = f"D{default_ref}"

        switch = add_regular_switch(switch_reference, switch_footprint, k)

        if (
            stabilizer_footprint
            and is_width_supported(k)
            and (k.width >= 2 or k.height >= 2)
        ):
            add_stabilizer(stab_reference, stabilizer_footprint, k)

        if layout_option == 0:
            diode = add_diode(diode_reference, diode_footprint)
            diodes[diode_reference] = diode
        else:
            diode = diodes[diode_reference]

        rows[row] += diode[1]
        columns[column] += switch[1]
        _ = switch[2] & diode[2]

        progress[position].append(switch_reference)

    return rows, columns

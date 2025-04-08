# SPDX-FileCopyrightText: 2025-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from typing import Dict, List, Optional

import skidl

# fmt: off
MINIMAL_POSITIONS = [
    { "ref":   "J1", "x":        0.0, "y":        0.0, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":       1.0 },
    { "ref":   "U1", "x":        0.0, "y":    7.14835, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":      2.45 },
]
MINIMAL_TRACKS = [
    { "x1":      -4.32, "y1":     -1.075, "x2":      -4.32, "y2":      3.105, "width":   0.4, "layer": "B.Cu" },
    { "x1":      -4.32, "y1":     -1.075, "x2":       4.32, "y2":     -1.075, "width":   0.4, "layer": "B.Cu" },
    { "x1":     -3.755, "y1":       3.67, "x2":      -4.32, "y2":      3.105, "width":   0.4, "layer": "B.Cu" },
    { "x1":      -3.35, "y1":       3.67, "x2":     -3.755, "y2":       3.67, "width":   0.4, "layer": "B.Cu" },
    { "x1":       -3.2, "y1":    6.14985, "x2":       -3.2, "y2":       3.67, "width":   0.4, "layer": "B.Cu" },
    { "x1":       -3.2, "y1":    6.14985, "x2":       -3.2, "y2":    6.15185, "width":   0.4, "layer": "B.Cu" },
    { "x1":       -2.4, "y1":    5.61335, "x2":       -2.4, "y2":       3.67, "width":   0.4, "layer": "B.Cu" },
    { "x1":       -2.4, "y1":    5.61335, "x2":       -2.4, "y2":    7.86335, "width":   0.4, "layer": "F.Cu" },
    { "x1":      -2.25, "y1":    2.87685, "x2":    -1.4865, "y2":    2.11335, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -2.25, "y1":       3.67, "x2":      -2.25, "y2":    2.87685, "width":   0.2, "layer": "B.Cu" },
    { "x1":    -2.2015, "y1":    7.14835, "x2":       -3.2, "y2":    6.14985, "width":   0.4, "layer": "B.Cu" },
    { "x1":    -1.4865, "y1":    2.11335, "x2":    1.51835, "y2":    2.11335, "width":   0.2, "layer": "B.Cu" },
    { "x1":    -1.1375, "y1":    5.41435, "x2":    -1.1375, "y2":    6.19835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    -1.1375, "y1":    7.14835, "x2":    -2.2015, "y2":    7.14835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    -1.1375, "y1":    9.83435, "x2":    -1.1375, "y2":    8.09835, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -0.75, "y1":      2.845, "x2":      -0.75, "y2":       3.67, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -0.75, "y1":       3.67, "x2":      -0.75, "y2":    5.02685, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -0.75, "y1":    5.02685, "x2":    -1.1375, "y2":    5.41435, "width":   0.2, "layer": "B.Cu" },
    { "x1":   -0.51835, "y1":    2.61335, "x2":      -0.75, "y2":      2.845, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -0.25, "y1":       3.67, "x2":      -0.25, "y2":      4.495, "width":   0.2, "layer": "B.Cu" },
    { "x1":      -0.25, "y1":      4.495, "x2":   -0.08165, "y2":    4.66335, "width":   0.2, "layer": "B.Cu" },
    { "x1":   -0.08165, "y1":    4.66335, "x2":    0.58165, "y2":    4.66335, "width":   0.2, "layer": "B.Cu" },
    { "x1":    0.01835, "y1":    2.61335, "x2":   -0.51835, "y2":    2.61335, "width":   0.2, "layer": "B.Cu" },
    { "x1":       0.25, "y1":      2.845, "x2":    0.01835, "y2":    2.61335, "width":   0.2, "layer": "B.Cu" },
    { "x1":       0.25, "y1":       3.67, "x2":       0.25, "y2":      2.845, "width":   0.2, "layer": "B.Cu" },
    { "x1":    0.58165, "y1":    4.66335, "x2":       0.75, "y2":      4.495, "width":   0.2, "layer": "B.Cu" },
    { "x1":       0.75, "y1":       3.67, "x2":       0.75, "y2":    4.99985, "width":   0.2, "layer": "B.Cu" },
    { "x1":       0.75, "y1":      4.495, "x2":       0.75, "y2":       3.67, "width":   0.2, "layer": "B.Cu" },
    { "x1":       0.75, "y1":    4.99985, "x2":     1.1375, "y2":    5.38735, "width":   0.2, "layer": "B.Cu" },
    { "x1":     1.1375, "y1":    5.38735, "x2":     1.1375, "y2":    6.19835, "width":   0.2, "layer": "B.Cu" },
    { "x1":     1.1375, "y1":    7.14835, "x2":       1.95, "y2":    7.14835, "width":   0.4, "layer": "B.Cu" },
    { "x1":     1.1375, "y1":    9.81935, "x2":     1.1375, "y2":    8.09835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    1.51835, "y1":    2.11335, "x2":       2.25, "y2":      2.845, "width":   0.2, "layer": "B.Cu" },
    { "x1":       1.95, "y1":    7.14835, "x2":        2.4, "y2":    6.69835, "width":   0.4, "layer": "B.Cu" },
    { "x1":       2.25, "y1":      2.845, "x2":       2.25, "y2":       3.67, "width":   0.2, "layer": "B.Cu" },
    { "x1":        2.4, "y1":    6.69835, "x2":        2.4, "y2":       3.67, "width":   0.4, "layer": "B.Cu" },
    { "x1":       3.35, "y1":       3.67, "x2":      3.755, "y2":       3.67, "width":   0.4, "layer": "B.Cu" },
    { "x1":      3.755, "y1":       3.67, "x2":       4.32, "y2":      3.105, "width":   0.4, "layer": "B.Cu" },
    { "x1":       4.32, "y1":     -1.075, "x2":       4.32, "y2":      3.105, "width":   0.4, "layer": "B.Cu" },
]
MINIMAL_TRACKS_FANOUT = {}
MINIMAL_VIAS = [
    { "x":    -2.4, "y":      5.61335, "width":        0.8, "hole":        0.4 },
]

UDB_CLONE_POSITIONS = [
    { "ref":     "D1", "x":       6.35, "y":      7.042, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":       0.0 },
    { "ref":     "F1", "x":      7.112, "y":      3.359, "rotation":  -90.0, "side":  "Back", "ref_x":       0.0, "ref_y":       0.0 },
    { "ref":     "J1", "x":        0.0, "y":        0.0, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":       0.0 },
    { "ref":     "R1", "x":     -3.048, "y":      7.281, "rotation":  -90.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":     "R2", "x":      3.048, "y":      7.281, "rotation":  -90.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":     "U1", "x":        0.0, "y":     6.1784, "rotation":   90.0, "side":  "Back", "ref_x":      -2.0, "ref_y":       1.5 },
]
UDB_CLONE_TRACKS = [
    { "x1":      -2.45, "y1":       3.72, "x2":      -2.45, "y2":      5.391, "width":      0.508, "layer": "B.Cu" },
    { "x1":     -2.206, "y1":      6.456, "x2":     -3.048, "y2":      6.456, "width":      0.254, "layer": "B.Cu" },
    { "x1":     -1.722, "y1":     5.3912, "x2":     -1.722, "y2":      5.972, "width":      0.254, "layer": "B.Cu" },
    { "x1":     -1.722, "y1":      5.972, "x2":     -2.206, "y2":      6.456, "width":      0.254, "layer": "B.Cu" },
    { "x1":      -1.27, "y1":      7.042, "x2":      -1.27, "y2":    8.64022, "width":     0.1524, "layer": "F.Cu" },
    { "x1":      -1.27, "y1":    8.64022, "x2":   -0.70802, "y2":     9.2022, "width":     0.1524, "layer": "F.Cu" },
    { "x1":      -1.25, "y1":      4.045, "x2":      -1.25, "y2":     4.9192, "width":      0.254, "layer": "B.Cu" },
    { "x1":      -1.25, "y1":     4.9192, "x2":     -1.722, "y2":     5.3912, "width":      0.254, "layer": "B.Cu" },
    { "x1":       -1.0, "y1":    5.24083, "x2":      -0.75, "y2":    4.99083, "width":     0.1524, "layer": "B.Cu" },
    { "x1":       -1.0, "y1":     6.5634, "x2":       -1.0, "y2":    5.24083, "width":     0.1524, "layer": "B.Cu" },
    { "x1":       -1.0, "y1":     6.5634, "x2":       -1.0, "y2":      6.772, "width":      0.254, "layer": "B.Cu" },
    { "x1":       -1.0, "y1":      6.772, "x2":      -1.27, "y2":      7.042, "width":      0.254, "layer": "B.Cu" },
    { "x1":      -0.75, "y1":    4.99083, "x2":      -0.75, "y2":      4.045, "width":     0.1524, "layer": "B.Cu" },
    { "x1":   -0.70802, "y1":     9.2022, "x2":    -0.0022, "y2":     9.2022, "width":     0.1524, "layer": "F.Cu" },
    { "x1":       -0.5, "y1":        5.4, "x2":      -0.25, "y2":       5.15, "width":      0.254, "layer": "B.Cu" },
    { "x1":       -0.5, "y1":        8.7, "x2":       -0.5, "y2":        5.4, "width":      0.254, "layer": "B.Cu" },
    { "x1":      -0.25, "y1":       5.15, "x2":      -0.25, "y2":      4.045, "width":      0.254, "layer": "B.Cu" },
    { "x1":    -0.0022, "y1":     9.2022, "x2":        0.5, "y2":        8.7, "width":     0.1524, "layer": "F.Cu" },
    { "x1":        0.0, "y1":     5.7934, "x2":        0.0, "y2":        7.4, "width":      0.254, "layer": "B.Cu" },
    { "x1":       0.25, "y1":       5.15, "x2":       0.25, "y2":      4.045, "width":      0.254, "layer": "B.Cu" },
    { "x1":        0.5, "y1":        5.4, "x2":       0.25, "y2":       5.15, "width":      0.254, "layer": "B.Cu" },
    { "x1":        0.5, "y1":        8.7, "x2":        0.5, "y2":        5.4, "width":      0.254, "layer": "B.Cu" },
    { "x1":      0.523, "y1":      7.677, "x2":       -0.5, "y2":        8.7, "width":     0.1524, "layer": "F.Cu" },
    { "x1":       0.75, "y1":    4.99083, "x2":       0.75, "y2":      4.045, "width":     0.1524, "layer": "B.Cu" },
    { "x1":        1.0, "y1":    5.24083, "x2":       0.75, "y2":    4.99083, "width":     0.1524, "layer": "B.Cu" },
    { "x1":        1.0, "y1":     6.5634, "x2":        1.0, "y2":    5.24083, "width":     0.1524, "layer": "B.Cu" },
    { "x1":        1.0, "y1":     6.5634, "x2":        1.0, "y2":      6.772, "width":      0.254, "layer": "B.Cu" },
    { "x1":        1.0, "y1":      6.772, "x2":       1.27, "y2":      7.042, "width":      0.254, "layer": "B.Cu" },
    { "x1":      1.016, "y1":      7.677, "x2":      0.523, "y2":      7.677, "width":     0.1524, "layer": "F.Cu" },
    { "x1":       1.27, "y1":      7.042, "x2":       1.27, "y2":      7.423, "width":     0.1524, "layer": "F.Cu" },
    { "x1":       1.27, "y1":      7.423, "x2":      1.016, "y2":      7.677, "width":     0.1524, "layer": "F.Cu" },
    { "x1":       1.75, "y1":       6.05, "x2":       1.75, "y2":      4.045, "width":      0.254, "layer": "B.Cu" },
    { "x1":      2.156, "y1":      6.456, "x2":       1.75, "y2":       6.05, "width":      0.254, "layer": "B.Cu" },
    { "x1":       2.45, "y1":       3.72, "x2":       2.45, "y2":      5.391, "width":      0.508, "layer": "B.Cu" },
    { "x1":       2.45, "y1":      5.391, "x2":      -2.45, "y2":      5.391, "width":      0.508, "layer": "F.Cu" },
    { "x1":       2.45, "y1":      5.391, "x2":    4.27065, "y2":      5.391, "width":      0.508, "layer": "B.Cu" },
    { "x1":      2.529, "y1":      9.201, "x2":      4.938, "y2":      9.201, "width":      0.508, "layer": "B.Cu" },
    { "x1":      3.048, "y1":      6.456, "x2":      2.156, "y2":      6.456, "width":      0.254, "layer": "B.Cu" },
    { "x1":    4.27065, "y1":      5.391, "x2":      5.325, "y2":    4.33665, "width":      0.508, "layer": "B.Cu" },
    { "x1":      4.938, "y1":      9.201, "x2":     5.7715, "y2":     8.3675, "width":      0.508, "layer": "B.Cu" },
    { "x1":      5.325, "y1":    2.51202, "x2":    5.87802, "y2":      1.959, "width":      0.508, "layer": "B.Cu" },
    { "x1":      5.325, "y1":    4.33665, "x2":      5.325, "y2":    2.51202, "width":      0.508, "layer": "B.Cu" },
    { "x1":     5.7715, "y1":     8.3675, "x2":     7.5825, "y2":     8.3675, "width":      0.508, "layer": "B.Cu" },
    { "x1":    5.87802, "y1":      1.959, "x2":      7.112, "y2":      1.959, "width":      0.508, "layer": "B.Cu" },
    { "x1":     7.5825, "y1":     8.3675, "x2":        8.0, "y2":       7.95, "width":      0.508, "layer": "B.Cu" },
    { "x1":        8.0, "y1":      5.647, "x2":      7.112, "y2":      4.759, "width":      0.508, "layer": "B.Cu" },
    { "x1":        8.0, "y1":      7.042, "x2":        8.0, "y2":      5.647, "width":      0.508, "layer": "B.Cu" },
    { "x1":        8.0, "y1":       7.95, "x2":        8.0, "y2":      7.042, "width":      0.508, "layer": "B.Cu" },
]
UDB_CLONE_VIAS = [
    { "x":      -2.45, "y":      5.391, "width":       0.45, "hole":     0.3048 },
    { "x":      -1.27, "y":      7.042, "width":       0.45, "hole":     0.3048 },
    { "x":       -0.5, "y":        8.7, "width":       0.45, "hole":     0.3048 },
    { "x":        0.0, "y":        7.4, "width":       0.45, "hole":     0.3048 },
    { "x":        0.5, "y":        8.7, "width":       0.45, "hole":     0.3048 },
    { "x":       1.27, "y":      7.042, "width":       0.45, "hole":     0.3048 },
    { "x":       2.45, "y":      5.391, "width":       0.45, "hole":     0.3048 },
]
# fmt: on

POSITIONS = {"minimal": MINIMAL_POSITIONS, "udb_clone": UDB_CLONE_POSITIONS}
TRACKS = {"minimal": MINIMAL_TRACKS, "udb_clone": UDB_CLONE_TRACKS}
TRACKS_FANOUT = {"minimal": MINIMAL_TRACKS_FANOUT, "udb_clone": {}}
VIAS = {"minimal": MINIMAL_VIAS, "udb_clone": UDB_CLONE_VIAS}


@skidl.subcircuit
def usb_minimal() -> skidl.Interface:
    # minimal, just usb connector and esd protection

    vcc = skidl.Net.fetch("VCC")
    gnd = skidl.Net.fetch("GND")

    usb = skidl.Part(
        "Connector",
        "USB_C_Receptacle_USB2.0_14P",
        footprint="Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
    )
    esd_protection = skidl.Part(
        "Power_Protection", "TPD2S017", footprint="Package_TO_SOT_SMD:SOT-23-6"
    )

    vcc += usb["VBUS"], esd_protection["VCC"]
    gnd += usb["GND", "SHIELD"], esd_protection["GND"]

    # we create nets manually to have names better than automatically generated
    usb_dm = skidl.Net("usb/D-")
    usb_dp = skidl.Net("usb/D+")
    usb_dm += usb["D-"], esd_protection["CH1In"]
    usb_dp += (
        usb["D+"],
        esd_protection["CH2Int"],
    )  # CH2Int -> bug in footprint pin name?

    # this net is fixed because we want to prioritize this name when connecting
    # other subcircuits to it
    esd_ref = esd_protection.ref.lower()
    usb_io_dm = skidl.Net(f"{esd_ref}/D-", fixed_name=True)
    usb_io_dp = skidl.Net(f"{esd_ref}/D+", fixed_name=True)
    usb_io_dm += esd_protection["CH1Out"]
    usb_io_dp += esd_protection["CH2Out"]

    return skidl.Interface(
        usb_io_dm=usb_io_dm,
        usb_io_dp=usb_io_dp,
    )


@skidl.subcircuit
def usb_udb_clone() -> skidl.Interface:
    # combination of https://github.com/Unified-Daughterboard/UDB-C-EZM and
    # https://github.com/Unified-Daughterboard/UDB-C-Legacy
    # (new UDB with 2-layer routing from older revision)

    vcc = skidl.Net.fetch("VCC")
    gnd = skidl.Net.fetch("GND")

    usb_footprint = "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12" # lcsc C165948
    usb = skidl.Part(
        "Connector",
        "USB_C_Receptacle_USB2.0_14P",
        footprint=usb_footprint,
    )

    esd_footprint = "Package_SON:USON-10_2.5x1.0mm_P0.5mm" # lcsc C138714
    esd_protection = skidl.Part(
        "Power_Protection", "TPD4E05U06DQA", footprint=esd_footprint
    )

    vbus = skidl.Net("VBUS")
    vbus += usb["VBUS"]
    gnd += usb["GND", "SHIELD"], esd_protection["GND"]

    usb_io_dm = skidl.Net("D-", fixed_name=True)
    usb_io_dp = skidl.Net("D+", fixed_name=True)

    usb_io_dm += usb["D-"], esd_protection["D1-"], esd_protection["D2-"]
    usb_io_dp += usb["D+"], esd_protection["D1+"], esd_protection["D2+"]

    R = skidl.Part(
        "Device",
        "R",
        skidl.TEMPLATE,
        footprint="Resistor_SMD:R_0603_1608Metric",
    )
    r1, r2 = R(num_copies=2, value="5.1k")
    _ = usb["CC1"] & r1 & gnd
    _ = usb["CC2"] & r2 & gnd

    f1 = skidl.Part("Device", "Polyfuse", footprint="Fuse:Fuse_1206_3216Metric")
    _ = vbus & f1 & vcc

    d1 = skidl.Part("Device", "D_Zener", footprint="Diode_SMD:D_SOD-123")
    vcc += d1[2]
    gnd += d1[1]

    return skidl.Interface(
        usb_io_dm=usb_io_dm,
        usb_io_dp=usb_io_dp,
    )


def positions(rev: str):
    return POSITIONS[rev]


def tracks(rev: str):
    return TRACKS[rev]


def fanout_tracks(rev: str):
    return {}


def vias(rev: str):
    return VIAS[rev]


def matrix_pins():
    return []


def add(rev: str) -> skidl.Interface:
    if rev == "minimal":
        return usb_minimal()
    elif rev == "udb_clone":
        return usb_udb_clone()
    msg = "Unexpected revision"
    raise RuntimeError(msg)


def default_revision() -> str:
    return "minimal"

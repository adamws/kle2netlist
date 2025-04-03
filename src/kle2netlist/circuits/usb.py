# SPDX-FileCopyrightText: 2025-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from typing import Dict, List, Optional

import skidl

V1_FOOTPRINTS = {
    "usb": "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
    "esd_protection": "Package_TO_SOT_SMD:SOT-23-6",
}

FOOTPRINTS = {"v1": V1_FOOTPRINTS}

# fmt: off
V1_POSITIONS = [
    { "ref":   "J1", "x":        0.0, "y":        0.0, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":       1.0 },
    { "ref":   "U1", "x":        0.0, "y":    7.14835, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":      2.45 },
]
V1_TRACKS = [
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
V1_TRACKS_FANOUT = {}
V1_VIAS = [
    { "x":    -2.4, "y":      5.61335 },
]
# fmt: on

POSITIONS = {"v1": V1_POSITIONS}
TRACKS = {"v1": V1_TRACKS}
TRACKS_FANOUT = {"v1": V1_TRACKS_FANOUT}
VIAS = {"v1": V1_VIAS}


@skidl.subcircuit
def usb(footprints) -> skidl.Interface:
    vcc = skidl.Net.fetch("VCC")
    gnd = skidl.Net.fetch("GND")

    usb = skidl.Part(
        "Connector",
        "USB_C_Receptacle_USB2.0_14P",
        footprint=footprints["usb"],
    )
    esd_protection = skidl.Part(
        "Power_Protection", "TPD2S017", footprint=footprints["esd_protection"]
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
    return usb(FOOTPRINTS[rev])

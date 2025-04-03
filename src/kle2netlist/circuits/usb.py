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
    { "ref":   "J1", "x":    24.4865, "y":   -5.86335, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":       1.0 },
    { "ref":   "U1", "x":    24.4865, "y":      1.285, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":      2.45 },
]
V1_TRACKS = [
    { "x1":    20.1665, "y1":   -6.93835, "x2":    20.1665, "y2":   -2.75835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    20.1665, "y1":   -6.93835, "x2":    28.8065, "y2":   -6.93835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    20.7315, "y1":   -2.19335, "x2":    20.1665, "y2":   -2.75835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    21.1365, "y1":   -2.19335, "x2":    20.7315, "y2":   -2.19335, "width":   0.4, "layer": "B.Cu" },
    { "x1":    21.2865, "y1":     0.2865, "x2":    21.2865, "y2":   -2.19335, "width":   0.4, "layer": "B.Cu" },
    { "x1":    21.2865, "y1":     0.2865, "x2":    21.2865, "y2":     0.2885, "width":   0.4, "layer": "B.Cu" },
    { "x1":    22.0865, "y1":      -0.25, "x2":    22.0865, "y2":   -2.19335, "width":   0.4, "layer": "B.Cu" },
    { "x1":    22.0865, "y1":      -0.25, "x2":    22.0865, "y2":        2.0, "width":   0.4, "layer": "F.Cu" },
    { "x1":    22.2365, "y1":    -2.9865, "x2":       23.0, "y2":      -3.75, "width":   0.2, "layer": "B.Cu" },
    { "x1":    22.2365, "y1":   -2.19335, "x2":    22.2365, "y2":    -2.9865, "width":   0.2, "layer": "B.Cu" },
    { "x1":     22.285, "y1":      1.285, "x2":    21.2865, "y2":     0.2865, "width":   0.4, "layer": "B.Cu" },
    { "x1":       23.0, "y1":      -3.75, "x2":   26.00485, "y2":      -3.75, "width":   0.2, "layer": "B.Cu" },
    { "x1":     23.349, "y1":     -0.449, "x2":     23.349, "y2":      0.335, "width":   0.2, "layer": "B.Cu" },
    { "x1":     23.349, "y1":      1.285, "x2":     22.285, "y2":      1.285, "width":   0.4, "layer": "B.Cu" },
    { "x1":     23.349, "y1":      3.971, "x2":     23.349, "y2":      2.235, "width":   0.2, "layer": "B.Cu" },
    { "x1":    23.7365, "y1":   -3.01835, "x2":    23.7365, "y2":   -2.19335, "width":   0.2, "layer": "B.Cu" },
    { "x1":    23.7365, "y1":   -2.19335, "x2":    23.7365, "y2":    -0.8365, "width":   0.2, "layer": "B.Cu" },
    { "x1":    23.7365, "y1":    -0.8365, "x2":     23.349, "y2":     -0.449, "width":   0.2, "layer": "B.Cu" },
    { "x1":   23.96815, "y1":      -3.25, "x2":    23.7365, "y2":   -3.01835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    24.2365, "y1":   -2.19335, "x2":    24.2365, "y2":   -1.36835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    24.2365, "y1":   -1.36835, "x2":   24.40485, "y2":       -1.2, "width":   0.2, "layer": "B.Cu" },
    { "x1":   24.40485, "y1":       -1.2, "x2":   25.06815, "y2":       -1.2, "width":   0.2, "layer": "B.Cu" },
    { "x1":   24.50485, "y1":      -3.25, "x2":   23.96815, "y2":      -3.25, "width":   0.2, "layer": "B.Cu" },
    { "x1":    24.7365, "y1":   -3.01835, "x2":   24.50485, "y2":      -3.25, "width":   0.2, "layer": "B.Cu" },
    { "x1":    24.7365, "y1":   -2.19335, "x2":    24.7365, "y2":   -3.01835, "width":   0.2, "layer": "B.Cu" },
    { "x1":   25.06815, "y1":       -1.2, "x2":    25.2365, "y2":   -1.36835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    25.2365, "y1":   -2.19335, "x2":    25.2365, "y2":    -0.8635, "width":   0.2, "layer": "B.Cu" },
    { "x1":    25.2365, "y1":   -1.36835, "x2":    25.2365, "y2":   -2.19335, "width":   0.2, "layer": "B.Cu" },
    { "x1":    25.2365, "y1":    -0.8635, "x2":     25.624, "y2":     -0.476, "width":   0.2, "layer": "B.Cu" },
    { "x1":     25.624, "y1":     -0.476, "x2":     25.624, "y2":      0.335, "width":   0.2, "layer": "B.Cu" },
    { "x1":     25.624, "y1":      1.285, "x2":    26.4365, "y2":      1.285, "width":   0.4, "layer": "B.Cu" },
    { "x1":     25.624, "y1":      3.956, "x2":     25.624, "y2":      2.235, "width":   0.2, "layer": "B.Cu" },
    { "x1":   26.00485, "y1":      -3.75, "x2":    26.7365, "y2":   -3.01835, "width":   0.2, "layer": "B.Cu" },
    { "x1":    26.4365, "y1":      1.285, "x2":    26.8865, "y2":      0.835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    26.7365, "y1":   -3.01835, "x2":    26.7365, "y2":   -2.19335, "width":   0.2, "layer": "B.Cu" },
    { "x1":    26.8865, "y1":      0.835, "x2":    26.8865, "y2":   -2.19335, "width":   0.4, "layer": "B.Cu" },
    { "x1":    27.8365, "y1":   -2.19335, "x2":    28.2415, "y2":   -2.19335, "width":   0.4, "layer": "B.Cu" },
    { "x1":    28.2415, "y1":   -2.19335, "x2":    28.8065, "y2":   -2.75835, "width":   0.4, "layer": "B.Cu" },
    { "x1":    28.8065, "y1":   -6.93835, "x2":    28.8065, "y2":   -2.75835, "width":   0.4, "layer": "B.Cu" },
]
V1_TRACKS_FANOUT = {}
V1_VIAS = [
    { "x":    22.0865, "y":      -0.25 },
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

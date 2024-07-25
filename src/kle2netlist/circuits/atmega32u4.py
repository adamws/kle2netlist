# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import skidl

ATMEGA32U4AU_PIN_ASSIGN_ORDER = [
    "PB0",
    "PB1",
    "PB2",
    "PB3",
    "PB4",
    "PB5",
    "PB6",
    "PB7",
    "PC6",
    "PC7",
    "PD0",
    "PD1",
    "PD2",
    "PD3",
    "PD4",
    "PD5",
    "PD6",
    "PD7",
    "PF0",
    "PF1",
    "PF4",
    "PF5",
    "PF6",
    "PF7",
]

V1_FOOTPRINTS = {
    "c_template": "Capacitor_SMD:C_0603_1608Metric",
    "r_template": "Resistor_SMD:R_0603_1608Metric",
    "uc": "Package_DFN_QFN:QFN-44-1EP_7x7mm_P0.5mm_EP5.2x5.2mm",
    "crystal": "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
    "usb": "Connector_USB:USB_C_Receptacle_XKB_U262-16XN-4BVC11",
    "esd_protection": "Package_TO_SOT_SMD:SOT-23-6",
    "button": "Button_Switch_SMD:SW_SPST_TL3342",
}
FOOTPRINTS = {"v1": V1_FOOTPRINTS}

# fmt: off
V1_POSITIONS = [
    { "ref":   "C1", "x":   -11.6355, "y":       -0.6, "rotation":  180.0, "side":  "Back", "ref_x":       0.0, "ref_y":       1.5 },
    { "ref":   "C2", "x":   -11.6355, "y":        1.6, "rotation":  180.0, "side":  "Back", "ref_x":       0.0, "ref_y":      -1.5 },
    { "ref":   "C3", "x":    -5.9205, "y":      3.952, "rotation":  180.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":   "C4", "x":     5.5095, "y":      2.775, "rotation":   90.0, "side":  "Back", "ref_x":       0.0, "ref_y":       1.5 },
    { "ref":   "C5", "x":     -2.775, "y":     -5.446, "rotation":  180.0, "side":  "Back", "ref_x":      -2.5, "ref_y":       0.0 },
    { "ref":   "C6", "x":     5.5095, "y":    -3.3505, "rotation":  -90.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":   "C7", "x":    -0.7135, "y":      5.857, "rotation":  180.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":   "C8", "x":     4.7602, "y":    5.86335, "rotation":    0.0, "side":  "Back", "ref_x":      -2.5, "ref_y":       0.0 },
    { "ref":   "J1", "x":    24.4865, "y":   -5.86335, "rotation":    0.0, "side":  "Back", "ref_x":      -4.0, "ref_y":       5.0 },
    { "ref":   "R1", "x":    17.6355, "y":      3.952, "rotation":    0.0, "side":  "Back", "ref_x":      -2.5, "ref_y":       0.0 },
    { "ref":   "R2", "x":    17.6355, "y":    5.86335, "rotation":    0.0, "side":  "Back", "ref_x":      -2.5, "ref_y":       0.0 },
    { "ref":   "R3", "x":     7.4145, "y":    -3.3505, "rotation":  -90.0, "side":  "Back", "ref_x":       2.5, "ref_y":       0.0 },
    { "ref":   "R4", "x":    -5.9205, "y":      5.857, "rotation":    0.0, "side":  "Back", "ref_x":      -2.5, "ref_y":       0.0 },
    { "ref":  "RST", "x":  -20.52725, "y":        0.0, "rotation":  180.0, "side":  "Back", "ref_x":       0.0, "ref_y":      3.75 },
    { "ref":   "U1", "x":        0.0, "y":        0.0, "rotation":   90.0, "side":  "Back", "ref_x":   2.87425, "ref_y":    -4.968 },
    { "ref":   "U2", "x":    24.4865, "y":      1.285, "rotation":    0.0, "side":  "Back", "ref_x":       0.0, "ref_y":      2.45 },
    { "ref":   "Y1", "x":    -7.9525, "y":        0.5, "rotation":  -90.0, "side":  "Back", "ref_x":       0.0, "ref_y":      -2.5 },
]
V1_TRACKS = [
    { "x1":        1.0, "y1":     3.3375, "x2":        1.0, "y2":     4.3237, "width":   0.2, "layer": 31 },
    { "x1":     1.7563, "y1":       5.08, "x2":      15.28, "y2":       5.08, "width":   0.2, "layer": 31 },
    { "x1":      15.28, "y1":       5.08, "x2":   16.06335, "y2":    5.86335, "width":   0.2, "layer": 31 },
    { "x1":        1.0, "y1":     4.3237, "x2":     1.7563, "y2":       5.08, "width":   0.2, "layer": 31 },
    { "x1":   16.06335, "y1":    5.86335, "x2":    16.8105, "y2":    5.86335, "width":   0.2, "layer": 31 },
    { "x1":    -7.9025, "y1":        0.5, "x2":    -8.8025, "y2":        1.4, "width":   0.2, "layer": 31 },
    { "x1":    -3.3375, "y1":        0.5, "x2":    -7.9025, "y2":        0.5, "width":   0.2, "layer": 31 },
    { "x1":   -10.8605, "y1":        1.6, "x2":    -8.8025, "y2":        1.6, "width":   0.2, "layer": 31 },
    { "x1":    -3.3375, "y1":        2.0, "x2":  -3.889386, "y2":        2.0, "width":   0.2, "layer": 31 },
    { "x1":  -17.37725, "y1":        1.9, "x2":     -13.34, "y2":        1.9, "width":   0.2, "layer": 31 },
    { "x1":    -4.3955, "y1":   2.506114, "x2":    -4.3955, "y2":   6.344648, "width":   0.2, "layer": 31 },
    { "x1":     -9.383, "y1":      5.857, "x2":    -6.7455, "y2":      5.857, "width":   0.2, "layer": 31 },
    { "x1":    -5.9025, "y1":        6.7, "x2":    -6.7455, "y2":      5.857, "width":   0.2, "layer": 31 },
    { "x1":  -3.889386, "y1":        2.0, "x2":    -4.3955, "y2":   2.506114, "width":   0.2, "layer": 31 },
    { "x1":     -13.34, "y1":        1.9, "x2":     -9.383, "y2":      5.857, "width":   0.2, "layer": 31 },
    { "x1":    -4.3955, "y1":   6.344648, "x2":  -4.750852, "y2":        6.7, "width":   0.2, "layer": 31 },
    { "x1":  -23.67725, "y1":        1.9, "x2":  -17.37725, "y2":        1.9, "width":   0.2, "layer": 31 },
    { "x1":  -4.750852, "y1":        6.7, "x2":    -5.9025, "y2":        6.7, "width":   0.2, "layer": 31 },
    { "x1":    24.7365, "y1":   -2.19335, "x2":    24.7365, "y2":   -3.01835, "width":   0.2, "layer": 31 },
    { "x1":     23.349, "y1":     -0.449, "x2":     23.349, "y2":      0.335, "width":   0.2, "layer": 31 },
    { "x1":    23.7365, "y1":   -3.01835, "x2":    23.7365, "y2":   -2.19335, "width":   0.2, "layer": 31 },
    { "x1":    23.7365, "y1":    -0.8365, "x2":     23.349, "y2":     -0.449, "width":   0.2, "layer": 31 },
    { "x1":    23.7365, "y1":   -2.19335, "x2":    23.7365, "y2":    -0.8365, "width":   0.2, "layer": 31 },
    { "x1":   24.50485, "y1":      -3.25, "x2":   23.96815, "y2":      -3.25, "width":   0.2, "layer": 31 },
    { "x1":    24.7365, "y1":   -3.01835, "x2":   24.50485, "y2":      -3.25, "width":   0.2, "layer": 31 },
    { "x1":   23.96815, "y1":      -3.25, "x2":    23.7365, "y2":   -3.01835, "width":   0.2, "layer": 31 },
    { "x1":       -0.5, "y1":     5.2955, "x2":     0.0615, "y2":      5.857, "width":   0.2, "layer": 31 },
    { "x1":     4.4595, "y1":        2.5, "x2":     5.5095, "y2":       3.55, "width":   0.2, "layer": 31 },
    { "x1":       -4.5, "y1":        1.5, "x2":    -3.3375, "y2":        1.5, "width":   0.2, "layer": 31 },
    { "x1":       -2.0, "y1":     -5.446, "x2":       -2.0, "y2":    -3.3375, "width":   0.2, "layer": 31 },
    { "x1":       -0.5, "y1":     3.3375, "x2":       -0.5, "y2":     5.2955, "width":   0.2, "layer": 31 },
    { "x1":      3.884, "y1":       -2.5, "x2":     5.5095, "y2":  -4.125498, "width":   0.2, "layer": 31 },
    { "x1":    -5.1455, "y1":      3.952, "x2":    -5.1455, "y2":      5.807, "width":   0.2, "layer": 31 },
    { "x1":    -5.1455, "y1":      3.952, "x2":    -5.1455, "y2":     2.1455, "width":   0.2, "layer": 31 },
    { "x1":     3.3375, "y1":        2.5, "x2":     4.4595, "y2":        2.5, "width":   0.2, "layer": 31 },
    { "x1":     3.3375, "y1":       -2.5, "x2":      3.884, "y2":       -2.5, "width":   0.2, "layer": 31 },
    { "x1":    -5.1455, "y1":     2.1455, "x2":       -4.5, "y2":        1.5, "width":   0.2, "layer": 31 },
    { "x1":   25.06815, "y1":       -1.2, "x2":    25.2365, "y2":   -1.36835, "width":   0.2, "layer": 31 },
    { "x1":    25.2365, "y1":    -0.8635, "x2":     25.624, "y2":     -0.476, "width":   0.2, "layer": 31 },
    { "x1":    25.2365, "y1":   -2.19335, "x2":    25.2365, "y2":    -0.8635, "width":   0.2, "layer": 31 },
    { "x1":    24.2365, "y1":   -1.36835, "x2":   24.40485, "y2":       -1.2, "width":   0.2, "layer": 31 },
    { "x1":   24.40485, "y1":       -1.2, "x2":   25.06815, "y2":       -1.2, "width":   0.2, "layer": 31 },
    { "x1":    25.2365, "y1":   -1.36835, "x2":    25.2365, "y2":   -2.19335, "width":   0.2, "layer": 31 },
    { "x1":    24.2365, "y1":   -2.19335, "x2":    24.2365, "y2":   -1.36835, "width":   0.2, "layer": 31 },
    { "x1":     25.624, "y1":     -0.476, "x2":     25.624, "y2":      0.335, "width":   0.2, "layer": 31 },
    { "x1":    -3.3375, "y1":        0.0, "x2":       -5.0, "y2":        0.0, "width":   0.2, "layer": 31 },
    { "x1":    -7.1025, "y1":       -0.6, "x2":       -5.6, "y2":       -0.6, "width":   0.2, "layer": 31 },
    { "x1":    -9.8605, "y1":       -1.6, "x2":  -8.002499, "y2":       -1.6, "width":   0.2, "layer": 31 },
    { "x1":  -8.002499, "y1":       -1.6, "x2":    -7.1025, "y2":       -0.7, "width":   0.2, "layer": 31 },
    { "x1":   -10.8605, "y1":       -0.6, "x2":    -9.8605, "y2":       -1.6, "width":   0.2, "layer": 31 },
    { "x1":       -5.6, "y1":       -0.6, "x2":       -5.0, "y2":        0.0, "width":   0.2, "layer": 31 },
    { "x1":   -11.3105, "y1":        0.5, "x2":   -12.4105, "y2":       -0.6, "width":   0.2, "layer": 31 },
    { "x1":   -11.4105, "y1":        2.6, "x2":  -8.002499, "y2":        2.6, "width":   0.2, "layer": 31 },
    { "x1":  -8.002499, "y1":        2.6, "x2":    -7.1025, "y2":        1.7, "width":   0.2, "layer": 31 },
    { "x1":     5.5095, "y1":        2.0, "x2":     3.3375, "y2":        2.0, "width":   0.2, "layer": 31 },
    { "x1":    -3.3375, "y1":        1.0, "x2":       -5.0, "y2":        1.0, "width":   0.2, "layer": 31 },
    { "x1":  -17.37725, "y1":       -1.9, "x2":   -13.7105, "y2":       -1.9, "width":   0.2, "layer": 31 },
    { "x1":     3.3375, "y1":       -2.0, "x2":        2.0, "y2":       -2.0, "width":   0.2, "layer": 31 },
    { "x1":       -2.5, "y1":    -3.3375, "x2":       -2.5, "y2":       -2.5, "width":   0.2, "layer": 31 },
    { "x1":   -12.4105, "y1":        1.6, "x2":   -11.4105, "y2":        2.6, "width":   0.2, "layer": 31 },
    { "x1":     3.3375, "y1":        2.0, "x2":        2.0, "y2":        2.0, "width":   0.2, "layer": 31 },
    { "x1":    -6.6955, "y1":     3.1445, "x2":    -6.6955, "y2":      3.952, "width":   0.2, "layer": 31 },
    { "x1":       -5.6, "y1":        1.6, "x2":       -5.0, "y2":        1.0, "width":   0.2, "layer": 31 },
    { "x1":        0.5, "y1":     3.3375, "x2":        0.5, "y2":        0.5, "width":   0.2, "layer": 31 },
    { "x1":     5.5095, "y1":    -2.5755, "x2":     7.3645, "y2":    -2.5755, "width":   0.2, "layer": 31 },
    { "x1":  -23.67725, "y1":       -1.9, "x2":  -17.37725, "y2":       -1.9, "width":   0.2, "layer": 31 },
    { "x1":    -8.8025, "y1":       -0.6, "x2":    -9.9025, "y2":        0.5, "width":   0.2, "layer": 31 },
    { "x1":    -9.9025, "y1":        0.5, "x2":   -11.3105, "y2":        0.5, "width":   0.2, "layer": 31 },
    { "x1":    -7.1025, "y1":        1.6, "x2":    -7.1025, "y2":     2.7375, "width":   0.2, "layer": 31 },
    { "x1":     3.3375, "y1":       -2.0, "x2":      4.934, "y2":       -2.0, "width":   0.2, "layer": 31 },
    { "x1":   -11.3105, "y1":        0.5, "x2":   -12.4105, "y2":        1.6, "width":   0.2, "layer": 31 },
    { "x1":   -13.7105, "y1":       -1.9, "x2":   -12.4105, "y2":       -0.6, "width":   0.2, "layer": 31 },
    { "x1":      4.934, "y1":       -2.0, "x2":     5.5095, "y2":    -2.5755, "width":   0.2, "layer": 31 },
    { "x1":       -2.5, "y1":     -4.396, "x2":      -3.55, "y2":     -5.446, "width":   0.2, "layer": 31 },
    { "x1":    -3.3375, "y1":        1.0, "x2":       -1.0, "y2":        1.0, "width":   0.2, "layer": 31 },
    { "x1":    -7.1025, "y1":        1.6, "x2":       -5.6, "y2":        1.6, "width":   0.2, "layer": 31 },
    { "x1":    -7.1025, "y1":     2.7375, "x2":    -6.6955, "y2":     3.1445, "width":   0.2, "layer": 31 },
    { "x1":       -2.5, "y1":    -3.3375, "x2":       -2.5, "y2":     -4.396, "width":   0.2, "layer": 31 },
    { "x1":    1.51335, "y1":    5.86335, "x2":     3.9852, "y2":    5.86335, "width":   0.2, "layer": 31 },
    { "x1":        0.0, "y1":       4.35, "x2":    1.51335, "y2":    5.86335, "width":   0.2, "layer": 31 },
    { "x1":        0.0, "y1":     3.3375, "x2":        0.0, "y2":       4.35, "width":   0.2, "layer": 31 },
    { "x1":      15.32, "y1":       4.68, "x2":  16.047999, "y2":      3.952, "width":   0.2, "layer": 31 },
    { "x1":  16.047999, "y1":      3.952, "x2":    16.8105, "y2":      3.952, "width":   0.2, "layer": 31 },
    { "x1":        1.5, "y1":     3.3375, "x2":        1.5, "y2":   4.258014, "width":   0.2, "layer": 31 },
    { "x1":   1.921986, "y1":       4.68, "x2":      15.32, "y2":       4.68, "width":   0.2, "layer": 31 },
    { "x1":        1.5, "y1":   4.258014, "x2":   1.921986, "y2":       4.68, "width":   0.2, "layer": 31 },
    { "x1":        2.5, "y1":  -4.188748, "x2":    3.18675, "y2":    -4.8755, "width":   0.2, "layer": 31 },
    { "x1":     6.7145, "y1":    -4.8755, "x2":     7.4145, "y2":    -4.1755, "width":   0.2, "layer": 31 },
    { "x1":        2.5, "y1":    -3.3375, "x2":        2.5, "y2":  -4.188748, "width":   0.2, "layer": 31 },
    { "x1":    3.18675, "y1":    -4.8755, "x2":     6.7145, "y2":    -4.8755, "width":   0.2, "layer": 31 },
]
# fmt: on

POSITIONS = {"v1": V1_POSITIONS}
TRACKS = {"v1": V1_TRACKS}


@skidl.subcircuit
def atmega32u4(rows, columns, footprints):
    assignment_order = ATMEGA32U4AU_PIN_ASSIGN_ORDER[:]
    num_rows = len(rows)
    num_columns = len(columns)
    num_pins = len(assignment_order)
    if num_rows + num_columns > num_pins:
        msg = (
            "Controller circuit with atmega32u4 can't handle requested matrix, "
            f"available pins: {num_pins}, required: "
            f"{num_rows} (rows) + {num_columns} (columns)"
        )
        raise RuntimeError(msg)

    # create templates
    C = skidl.Part(
        "Device",
        "C",
        skidl.TEMPLATE,
        footprint=footprints["c_template"],
    )
    R = skidl.Part(
        "Device",
        "R",
        skidl.TEMPLATE,
        footprint=footprints["r_template"],
    )

    # start uc circuitry
    uc = skidl.Part(
        "MCU_Microchip_ATmega",
        "ATmega32U4-M",
        footprint=footprints["uc"],
    )
    vcc = skidl.Net("VCC")
    gnd = skidl.Net("GND")

    vcc += uc["UVCC", "VCC", "AVCC", "VBUS"]
    gnd += uc["UGND", "GND"]

    # crystal oscillator
    crystal = skidl.Part(
        "Device",
        "Crystal_GND24",
        footprint=footprints["crystal"],
    )
    c1, c2 = C(num_copies=2, value="22p")

    net_xtal1 = skidl.Net("mcu/XTAL1")
    net_xtal1 += c1[1], crystal[1], uc["XTAL1"]
    net_xtal2 = skidl.Net("mcu/XTAL2")
    net_xtal2 += c2[1], crystal[3], uc["XTAL2"]
    gnd += c1[2], c2[2], crystal[2], crystal[4]

    # decoupling capacitors, 0.1u for each pin (as recommended in datasheet)
    # and one bigger for VBUS, some designs use less and work just as well
    c3, c4, c5, c6 = C(num_copies=4, value="0.1u")
    c7 = C(value="4.7u")  # could be 10u

    for c in [c3, c4, c5, c6, c7]:
        vcc += c[1]
        gnd += c[2]

    # ucap
    c8 = C(value="1u")
    net_ucap = skidl.Net("mcu/UCAP")
    net_ucap += c8[1], uc["UCAP"]
    gnd += c8[2]

    # usb
    usb = skidl.Part(
        "Connector",
        "USB_C_Receptacle_USB2.0_14P",
        footprint=footprints["usb"],
    )
    esd_protection = skidl.Part(
        "Power_Protection", "TPD2S017", footprint=footprints["esd_protection"]
    )
    r1, r2 = R(num_copies=2, value="22")

    vcc += usb["VBUS"], esd_protection["VCC"]
    gnd += usb["GND", "SHIELD"], esd_protection["GND"]

    net_usb_dm = skidl.Net("usb/D-")
    net_usb_dm += usb["D-"], esd_protection["CH1In"]

    net_usb_dp = skidl.Net("usb/D+")
    net_usb_dp += (
        usb["D+"],
        esd_protection["CH2Int"],
    )  # CH2Int -> bug in footprint pin name?

    net_esd_dm = skidl.Net("u2/D-")
    net_esd_dm += esd_protection["CH1Out"], r1[2]

    net_esd_dp = skidl.Net("u2/D+")
    net_esd_dp += esd_protection["CH2Out"], r2[2]

    net_uc_dm = skidl.Net("mcu/D-")
    net_uc_dm += r1[1], uc["D-"]

    net_uc_dp = skidl.Net("mcu/D+")
    net_uc_dp += r2[1], uc["D+"]

    # pe2 and reset
    r3, r4 = R(num_copies=2, value="10k")
    button = skidl.Part(
        "Switch",
        "SW_SPST",
        footprint=footprints["button"],
        ref="RST",
    )

    net_hwb = skidl.Net("mcu/~{HWB}/PE2")
    net_hwb += uc["~{HWB}/PE2"], r3[1]
    gnd += r3[2]

    net_reset = skidl.Net("mcu/~{RESET}")
    net_reset += uc["~{RESET}"], r4[1], button[2]
    vcc += r4[2]
    gnd += button[1]

    for _, row in rows.items():
        row += uc[assignment_order.pop(0)]
    for _, column in columns.items():
        column += uc[assignment_order.pop(0)]


def atmega32u4_au_v1(rows, columns):
    atmega32u4(rows, columns, FOOTPRINTS["v1"])


if __name__ == "__main__":
    import argparse

    import pcbnew

    from kle2netlist.pcb import Footprint, Track, add_tracks, set_positions
    from kle2netlist.skidl import set_skidl_search_path

    parser = argparse.ArgumentParser(description="Generate kicad_pcb templates")
    parser.add_argument(
        "--variant",
        required=False,
        default="v1",
        choices=["v1"],
        help="Choose variant",
    )

    args = parser.parse_args()
    variant = args.variant

    set_skidl_search_path()

    circuit = skidl.Circuit()
    with circuit:
        atmega32u4({}, {}, FOOTPRINTS[variant])

    libraries = ["/usr/share/kicad/footprints"]
    board_path = f"atmega32u4_au_{variant}.kicad_pcb"
    circuit.generate_pcb(file_=board_path, fp_libs=libraries)

    board = pcbnew.LoadBoard(board_path)
    set_positions(board, [Footprint.fromdict(d) for d in POSITIONS[variant]])
    add_tracks(board, [Track.fromdict(d) for d in TRACKS[variant]])
    pcbnew.SaveBoard(board_path, board)

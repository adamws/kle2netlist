# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from copy import copy

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
    "uc": "Package_QFP:TQFP-44_10x10mm_P0.8mm",
    "crystal": "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
    "usb": "Connector_USB:USB_C_Receptacle_XKB_U262-16XN-4BVC11",
    "esd_protection": "Package_TO_SOT_SMD:SOT-23-6",
    "button": "Button_Switch_SMD:SW_SPST_TL3342",
}
V2_FOOTPRINTS = copy(V1_FOOTPRINTS)
V2_FOOTPRINTS["uc"] = "Package_DFN_QFN:QFN-44-1EP_7x7mm_P0.5mm_EP5.2x5.2mm"

FOOTPRINTS = {"v1": V1_FOOTPRINTS, "v2": V2_FOOTPRINTS}

# fmt: off
V1_POSITIONS = [
    { "ref":   "C1", "x": 34.01, "y":    1.69, "rotation":   45.0, "side": "Back", "ref_x":       0.0, "ref_y":      1.43 },
    { "ref":   "C2", "x": 33.65, "y":   -2.78, "rotation":  -45.0, "side": "Back", "ref_x":  0.070711, "ref_y": -1.414214 },
    { "ref":   "C3", "x": 11.58, "y":    4.24, "rotation":  180.0, "side": "Back", "ref_x":       0.0, "ref_y":      1.43 },
    { "ref":   "C4", "x": 21.29, "y":   -8.15, "rotation":  180.0, "side": "Back", "ref_x":     -2.51, "ref_y":      0.01 },
    { "ref":   "C5", "x":  24.2, "y":    9.37, "rotation":  -90.0, "side": "Back", "ref_x":       0.0, "ref_y":      1.43 },
    { "ref":   "C6", "x": 11.58, "y":    -3.7, "rotation":  180.0, "side": "Back", "ref_x":      0.06, "ref_y":     -1.47 },
    { "ref":   "C7", "x": 16.97, "y":   -8.15, "rotation":  180.0, "side": "Back", "ref_x":       0.0, "ref_y":      1.43 },
    { "ref":   "C8", "x": 21.29, "y":   -9.74, "rotation":  180.0, "side": "Back", "ref_x":     -2.55, "ref_y":      0.04 },
    { "ref":   "J1", "x": 18.75, "y": -27.275, "rotation":    0.0, "side": "Back", "ref_x":       0.0, "ref_y":     5.715 },
    { "ref":   "R1", "x": 17.85, "y":  -12.28, "rotation":   90.0, "side": "Back", "ref_x":     -0.03, "ref_y":      3.33 },
    { "ref":   "R2", "x": 19.55, "y":  -12.27, "rotation":   90.0, "side": "Back", "ref_x":       0.0, "ref_y":      2.86 },
    { "ref":   "R3", "x": 16.96, "y":    9.37, "rotation":  -90.0, "side": "Back", "ref_x":       0.0, "ref_y":      1.43 },
    { "ref":   "R4", "x": 32.01, "y":   -5.39, "rotation": -135.0, "side": "Back", "ref_x": -2.453661, "ref_y":  -0.13435 },
    { "ref":  "RST", "x": 41.75, "y":    -6.0, "rotation":   90.0, "side": "Back", "ref_x":       0.0, "ref_y":      3.75 },
    { "ref":   "U1", "x": 20.98, "y":    0.25, "rotation":  -90.0, "side": "Back", "ref_x":       0.0, "ref_y":      7.45 },
    { "ref":   "U2", "x":  18.7, "y": -18.375, "rotation":    0.0, "side": "Back", "ref_x":       0.0, "ref_y":       2.9 },
    { "ref":   "Y1", "x":  31.6, "y":   -0.68, "rotation":  135.0, "side": "Back", "ref_x": -1.230366, "ref_y": -2.446589 },
]
# fmt: on

POSITIONS = {"v1": V1_POSITIONS, "v2": None}


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
        "ATmega32U4-A",
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


def atmega32u4_au_v2(rows, columns):
    atmega32u4(rows, columns, FOOTPRINTS["v2"])


if __name__ == "__main__":
    import pcbnew

    from kle2netlist.pcb import Footprint, set_positions
    from kle2netlist.skidl import set_skidl_search_path

    set_skidl_search_path()

    circuit = skidl.Circuit()
    with circuit:
        atmega32u4_au_v1({}, {})

    libraries = ["/usr/share/kicad/footprints"]
    board_path = "atmega32u4_au_v1.kicad_pcb"
    circuit.generate_pcb(file_=board_path, fp_libs=libraries)

    board = pcbnew.LoadBoard(board_path)
    set_positions(board, [Footprint.fromdict(d) for d in POSITIONS["v1"]])
    pcbnew.SaveBoard(board_path, board)

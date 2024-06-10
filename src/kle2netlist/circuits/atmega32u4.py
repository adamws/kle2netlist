# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import sys

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


@skidl.subcircuit
def atmega32u4_au_v1(rows, columns):
    assignment_order = ATMEGA32U4AU_PIN_ASSIGN_ORDER[:]
    variant = "atmega32u4_au_v1"
    num_rows = len(rows)
    num_columns = len(columns)
    num_pins = len(assignment_order)
    if num_rows + num_columns > num_pins:
        msg = (
            f"Controller circuit '{variant}' can't handle requested matrix, "
            f"available pins: {num_pins}, required: "
            f"{num_rows} (rows) + {num_columns} (columns)"
        )
        raise RuntimeError(msg)

    # create templates
    C = skidl.Part(
        "Device",
        "C",
        skidl.TEMPLATE,
        footprint="Capacitor_SMD:C_0603_1608Metric",
    )
    R = skidl.Part(
        "Device",
        "R",
        skidl.TEMPLATE,
        footprint="Resistor_SMD:R_0603_1608Metric",
    )

    # start uc circuitry
    uc = skidl.Part(
        "MCU_Microchip_ATmega",
        "ATmega32U4-A",
        footprint="Package_QFP:TQFP-44_10x10mm_P0.8mm",
    )
    vcc = skidl.Net("VCC")
    gnd = skidl.Net("GND")

    vcc += uc["UVCC", "VCC", "AVCC", "VBUS"]
    gnd += uc["UGND", "GND"]

    # crystal oscillator
    crystal = skidl.Part(
        "Device",
        "Crystal_GND24",
        footprint="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
    )
    c1, c2 = C(num_copies=2, value="22p")

    net_xtal1 = skidl.Net("mcu/XTAL1")
    net_xtal1 += c1[1], crystal[1], uc["XTAL1"]
    net_xtal2 = skidl.Net("mcu/XTAL2")
    net_xtal2 += c2[1], crystal[3], uc["XTAL2"]
    gnd += c1[2], c2[2], crystal[2], crystal[4]

    # decoupling capacitors
    c3, c4, c5, c6 = C(num_copies=4, value="0.1u")
    c7 = C(value="4.7u")

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
        footprint="Connector_USB:USB_C_Receptacle_XKB_U262-16XN-4BVC11",
    )
    esd_protection = skidl.Part(
        "Power_Protection", "TPD2S017", footprint="Package_TO_SOT_SMD:SOT-23-6"
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
        footprint="Button_Switch_SMD:SW_SPST_TL3342",
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

# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import bisect
import importlib.resources
import re
import sys

import skidl

KISWITCH_LIBRARY_METADATA = {
    "modules": {
        "MX": {
            "name": "Switch_Keyboard_Cherry_MX",
            "footprint-nameformat": "SW_Cherry_MX_PCB_{:.2f}u",
            "iso-enter": "SW_Cherry_MX_PCB_ISOEnter",
        },
        "Alps": {
            "name": "Switch_Keyboard_Alps_Matias",
            "footprint-nameformat": "SW_Alps_Matias_{:.2f}u",
            "iso-enter": "SW_Alps_Matias_ISOEnter",
        },
        "MX/Alps Hybrid": {
            "name": "Switch_Keyboard_Hybrid",
            "footprint-nameformat": "SW_Hybrid_Cherry_MX_Alps_{:.2f}u",
            "iso-enter": "SW_Hybrid_Cherry_MX_Alps_ISOEnter",
        },
        "Hotswap Kailh MX": {
            "name": "Switch_Keyboard_Hotswap_Kailh",
            "footprint-nameformat": "SW_Hotswap_Kailh_MX_{:.2f}u",
            "iso-enter": "SW_Hotswap_Kailh_MX_ISOEnter",
        }
    },
    "supported-widths": [
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
    ],
    "supported-stabilizers": [
        2,
        3,
        6,
        6.25,
        7,
        8,
    ],
}

SUPPORTED_LIBRARIES = {
    "ai03-2725/MX_Alps_Hybrid": {
        "modules": {
            "MX": {
                "name": "MX_Only",
                "footprint-nameformat": "MXOnly-{:g}U-NoLED",
                "iso-enter": "MXOnly-ISO",
            },
            "Alps": {
                "name": "Alps_Only",
                "footprint-nameformat": "ALPS-{:g}U",
            },
            "MX/Alps Hybrid": {
                "name": "MX_Alps_Hybrid",
                "footprint-nameformat": "MX-{:g}U-NoLED",
                "iso-enter": "MX-ISO",
            },
        },
        "supported-widths": [
            1,
            1.25,
            1.5,
            1.75,
            2,
            2.25,
            2.5,
            2.75,
            3,
            6,
            6.25,
            6.5,
            7,
            8,
            9,
            10,
        ],
        "supported-stabilizers": [],  # stabilizers are part of switch footprint
    },
    # tested with https://github.com/perigoso/keyswitch-kicad-library/releases/tag/v2.2
    "perigoso/keyswitch-kicad-library": KISWITCH_LIBRARY_METADATA,
    # perigoso library has been moved to new location:
    # tested with https://github.com/kiswitch/keyswitch-kicad-library/releases/tag/v2.4
    "kiswitch/keyswitch-kicad-library": KISWITCH_LIBRARY_METADATA,
}

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


def is_iso_enter(key):
    key_width = float(key["width"])
    key_height = float(key["height"])
    key_width_2 = float(key["width2"])
    key_height_2 = float(key["height2"])
    return (
        key_width == 1.25
        and key_height == 2
        and key_width_2 == 1.5
        and key_height_2 == 1
    )


def find_closest_smaller_or_equal(lst, target):
    index = bisect.bisect_right(lst, target)
    if index == 0:
        return None  # No value is smaller or equal
    else:
        return lst[index - 1]


def add_stabilizer(reference, key_width):
    # this function works only for perigoso/keyswitch-kicad-library
    supported_stabilizer_size = SUPPORTED_LIBRARIES["perigoso/keyswitch-kicad-library"][
        "supported-stabilizers"
    ]
    stabilizer_width = find_closest_smaller_or_equal(
        supported_stabilizer_size, key_width
    )

    if stabilizer_width:
        stabilizer_footprint = (
            f"Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{stabilizer_width:.2f}u"
        )
        stabilizer = skidl.Part(
            "Mechanical", "MountingHole", footprint=stabilizer_footprint
        )
        stabilizer.ref = reference


def add_iso_enter_switch(switch_module, diode_footprint):
    module_name = switch_module["name"]

    try:
        switch_footprint = switch_module["iso-enter"]
    except KeyError:
        footprint_format = switch_module["footprint-nameformat"]
        switch_footprint = f"{footprint_format}".format(1)

    switch_footprint = f"{module_name}:{switch_footprint}"

    switch = skidl.Part("Switch", "SW_Push", footprint=switch_footprint)
    diode = skidl.Part("Device", "D", footprint=f"Diode_SMD:{diode_footprint}")

    if module_name in ["Switch_Keyboard_Cherry_MX", "Switch_Keyboard_Hybrid"]:
        stabilizer_footprint = "Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_2.00u"
        stabilizer = skidl.Part(
            "Mechanical", "MountingHole", footprint=stabilizer_footprint
        )
        switch_reference_number = switch.ref[2:]
        stabilizer.ref = f"ST{switch_reference_number}"

    return switch, diode


def add_regular_switch(switch_module, key_width, diode_footprint):
    footprint_format = switch_module["footprint-nameformat"]
    module_name = switch_module["name"]

    switch_footprint = f"{footprint_format}".format(key_width)
    switch_footprint = f"{module_name}:{switch_footprint}"

    switch = skidl.Part("Switch", "SW_Push", footprint=switch_footprint)
    diode = skidl.Part("Device", "D", footprint=f"Diode_SMD:{diode_footprint}")

    if (
        module_name in ["Switch_Keyboard_Cherry_MX", "Switch_Keyboard_Hybrid"]
        and key_width >= 2
    ):
        switch_reference_number = switch.ref[2:]
        add_stabilizer(f"ST{switch_reference_number}", key_width)

    return switch, diode


def is_key_label_valid(label):
    if label and re.match(r"^[0-9]+,[0-9]+$", label):
        return True
    else:
        return False


def handle_switch_matrix(keys, switch_module, supported_widths, diode_footprint):
    rows = {}
    columns = {}

    for key in keys:
        labels = key["labels"]
        if not labels:
            msg = "Key labels missing"
            raise RuntimeError(msg)

        # be forgiving, remove all whitespaces to fix simple mistakes:
        labels[0] = re.sub(r"\s+", "", str(labels[0]), flags=re.UNICODE)

        if not is_key_label_valid(labels[0]):
            msg = (
                f"Key label invalid: '{labels[0]}' - "
                "label needs to follow 'row,column' format, for example '1,2'"
            )
            raise RuntimeError(msg)

        row, column = map(int, labels[0].split(","))

        if row not in rows:
            rows[row] = skidl.Net(f"ROW{row}")
        if column not in columns:
            columns[column] = skidl.Net(f"COL{column}")

        if is_iso_enter(key):
            switch, diode = add_iso_enter_switch(switch_module, diode_footprint)
        else:
            key_width = float(key["width"])
            switch, diode = add_regular_switch(
                switch_module,
                key_width if key_width in supported_widths else 1,
                diode_footprint,
            )

        rows[row] += diode[1]
        columns[column] += switch[1]
        _ = switch[2] & diode[2]

    return rows, columns


def add_controller_atmega32u4_au_v1():
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
        "USB_C_Receptacle_USB2.0",
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

    return uc


def add_controller_circuit(variant, rows, columns):
    uc = add_controller_atmega32u4_au_v1()
    pins = ATMEGA32U4AU_PIN_ASSIGN_ORDER[:]
    num_rows = len(rows)
    num_columns = len(columns)
    num_pins = len(pins)
    if num_rows + num_columns > num_pins:
        msg = (
            f"Controller circuit '{variant}' can't handle requested matrix, "
            f"available pins: {num_pins}, required: "
            f"{num_rows} (rows) + {num_columns} (columns)"
        )
        raise RuntimeError(msg)

    for _, row in rows.items():
        row += uc[pins.pop(0)]
    for _, column in columns.items():
        column += uc[pins.pop(0)]


def build_circuit(layout, **kwargs):
    default_circuit.reset()
    additional_search_path = kwargs.get("additional_search_path")
    if additional_search_path:
        for path in additional_search_path:
            skidl.lib_search_paths[skidl.KICAD].append(path)

    # try using bundled symbols as fallback:
    if sys.version_info[1] == 10:
        with importlib.resources.path("kle2netlist", "data") as p:
            default_search_path = p.joinpath("kicad-symbols")
    else:
        # for python <3.9 you can't use directory as resource:
        with importlib.resources.path("kle2netlist", "skidl.py") as p:
            default_search_path = p.parent.joinpath("data/kicad-symbols")
    skidl.lib_search_paths[skidl.KICAD].append(default_search_path)

    try:
        switch_library = kwargs.get("switch_library")
        library = SUPPORTED_LIBRARIES[switch_library]

        switch_footprint = kwargs.get("switch_footprint")
        diode_footprint = kwargs.get("diode_footprint")
        switch_module = library["modules"][switch_footprint]
        supported_widths = library["supported-widths"]

    except KeyError as err:
        msg = "Unsupported argument"
        raise RuntimeError(msg) from err

    rows, columns = handle_switch_matrix(
        layout["keys"], switch_module, supported_widths, diode_footprint
    )

    if kwargs.get("controller_circuit"):
        add_controller_circuit("atmega32u4_au_v1", rows, columns)


def generate_netlist(output, netlist_type="net"):
    if netlist_type == "net":
        skidl.generate_netlist(file_=output)
    elif netlist_type == "xml":
        skidl.generate_xml(file_=output)
    else:
        msg = f"Unsupported netlist type: {netlist_type}"
        raise RuntimeError(msg)


__all__ = ["build_circuit", "generate_netlist"]

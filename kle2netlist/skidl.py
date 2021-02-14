import math

import skidl

SUPPORTED_LIBRARIES = {
    "ai03-2725/MX_Alps_Hybrid": {
        "source": "https://github.com/ai03-2725/MX_Alps_Hybrid",
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
    },
    "perigoso/Switch_Keyboard": {
        "source": "https://github.com/perigoso/Switch_Keyboard",
        "modules": {
            "MX": {
                "name": "Switch_Keyboard_Cherry_MX",
                "footprint-nameformat": "SW_Cherry_MX_PCB_{:.2f}u",
                "iso-enter": "SW_Cherry_MX_PCB_ISOEnter_Rotated90",
            },
            "Alps": {
                "name": "Switch_Keyboard_Alps_Matias",
                "footprint-nameformat": "SW_Alps_Matias_{:.2f}u",
            },
            "MX/Alps Hybrid": {
                "name": "Switch_Keyboard_Hybrid",
                "footprint-nameformat": "SW_Hybrid_Cherry_MX_Alps_{:.2f}u",
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
            4,
            4.5,
            5,
            5.5,
            6,
            6.25,
            6.5,
            7,
        ],
    },
}


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


def add_stabilizer(reference, key_width):
    stabilizer_footprint = (
        "Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{:d}u".format(
            math.trunc(key_width)
        )
    )
    stabilizer = skidl.Part(
        "Mechanical", "MountingHole", footprint=stabilizer_footprint
    )
    stabilizer.ref = reference


def add_iso_enter_switch(switch_module):
    module_name = switch_module["name"]

    try:
        switch_footprint = switch_module["iso-enter"]
    except KeyError:
        footprint_format = switch_module["footprint-nameformat"]
        switch_footprint = f"{footprint_format}".format(1)

    switch_footprint = f"{module_name}:{switch_footprint}"

    switch = skidl.Part("Switch", "SW_Push", footprint=switch_footprint)
    diode = skidl.Part("Device", "D", footprint="Diode_SMD:D_SOD-323F")

    if (
        module_name == "Switch_Keyboard_Cherry_MX"
        or module_name == "Switch_Keyboard_Hybrid"
    ):
        stabilizer_footprint = (
            "Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_2u"
        )
        stabilizer = skidl.Part(
            "Mechanical", "MountingHole", footprint=stabilizer_footprint
        )
        switch_reference_number = switch.ref[2:]
        stabilizer.ref = f"ST{switch_reference_number}"

    return switch, diode


def add_regular_switch(switch_module, key_width):
    footprint_format = switch_module["footprint-nameformat"]
    module_name = switch_module["name"]

    switch_footprint = f"{footprint_format}".format(key_width)
    switch_footprint = f"{module_name}:{switch_footprint}"

    switch = skidl.Part("Switch", "SW_Push", footprint=switch_footprint)
    diode = skidl.Part("Device", "D", footprint="Diode_SMD:D_SOD-323F")

    if (
        module_name == "Switch_Keyboard_Cherry_MX"
        or module_name == "Switch_Keyboard_Hybrid"
    ) and key_width >= 2:
        switch_reference_number = switch.ref[2:]
        add_stabilizer(f"ST{switch_reference_number}", key_width)

    return switch, diode


def handle_switch_matrix(keys, switch_module, supported_widths):
    rows = {}
    columns = {}

    for key in keys:
        labels = key["labels"]
        if not labels:
            raise RuntimeError("Key label for matrix position missing")

        row, column = map(int, labels[0].split(","))
        if not row in rows:
            rows[row] = skidl.Net(f"ROW{row}")
        if not column in columns:
            columns[column] = skidl.Net(f"COL{column}")

        if is_iso_enter(key):
            switch, diode = add_iso_enter_switch(switch_module)
        else:
            key_width = float(key["width"])
            switch, diode = add_regular_switch(
                switch_module, key_width if key_width in supported_widths else 1
            )

        rows[row] += diode[1]
        columns[column] += switch[1]
        _ = switch[2] & diode[2]


def kle2netlist(layout, output_path, **kwargs):
    default_circuit.reset()

    additional_search_path = kwargs.get("additional_search_path")
    for path in additional_search_path:
        skidl.lib_search_paths[skidl.KICAD].append(path)

    try:
        switch_library = kwargs.get("switch_library")
        library = SUPPORTED_LIBRARIES[switch_library]

        switch_footprint = kwargs.get("switch_footprint")
        switch_module = library["modules"][switch_footprint]
        supported_widths = library["supported-widths"]

    except KeyError as err:
        raise RuntimeError("Unsupported argument") from err

    handle_switch_matrix(layout["keys"], switch_module, supported_widths)

    skidl.generate_netlist(file_=output_path)


__all__ = ["kle2netlist"]

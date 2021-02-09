import math

import skidl

SUPPORTED_LIBRARIES = {
    "ai03-2725/MX_Alps_Hybrid": {
        "source": "https://github.com/ai03-2725/MX_Alps_Hybrid",
        "modules": {
            "MX": {
                "name": "MX_Only",
                "footprint-nameformat": "MXOnly-{:g}U-NoLED",
            },
            "Alps": {
                "name": "Alps_Only",
                "footprint-nameformat": "ALPS-{:g}U",
            },
            "MX/Alps Hybrid": {
                "name": "MX_Alps_Hybrid",
                "footprint-nameformat": "MX-{:g}U-NoLED",
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


def handle_key_matrix(keys, switch_module, supported_widths):
    module_name = switch_module["name"]
    footprint_format = switch_module["footprint-nameformat"]

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

        key_width = float(key["width"])
        if key_width not in supported_widths:
            key_width = 1

        switch_footprint = f"{footprint_format}".format(key_width)
        switch_footprint = f"{module_name}:{switch_footprint}"

        switch = skidl.Part("Switch", "SW_Push", footprint=switch_footprint)
        diode = skidl.Part("Device", "D", footprint="Diode_SMD:D_SOD-323F")

        if (
            module_name == "Switch_Keyboard_Cherry_MX"
            or module_name == "Switch_Keyboard_Hybrid"
        ) and key_width >= 2:
            stabilizer_footprint = "Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{:d}u".format(
                math.trunc(key_width)
            )
            stabilizer = skidl.Part(
                "Mechanical", "MountingHole", footprint=stabilizer_footprint
            )
            stabilizer_reference = switch.ref[2:]
            stabilizer.ref = f"ST{stabilizer_reference}"

        rows[row] += diode[1]
        columns[column] += switch[1]
        _ = switch[2] & diode[2]


def kle2netlist(layout, output_path, **kwargs):
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

    handle_key_matrix(layout["keys"], switch_module, supported_widths)

    skidl.generate_netlist(file_=output_path)


__all__ = ["kle2netlist"]

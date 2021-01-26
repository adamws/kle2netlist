from skidl import *

SUPPORTED_LIBRARIES = {
    "MX_Alps_Hybrid": {
        "source": "https://github.com/ai03-2725/MX_Alps_Hybrid",
        "modules": ["MX_Only"],
        "MX_Only": {
            "footprints": [
                "MXOnly-1U-NoLED",
                "MXOnly-1.25U-NoLED",
                "MXOnly-1.5U-NoLED",
                "MXOnly-1.75U-NoLED",
                "MXOnly-2U-NoLED",
                "MXOnly-2.25U-NoLED",
                "MXOnly-2.5U-NoLED",
                "MXOnly-2.75U-NoLED",
                "MXOnly-3U-NoLED",
                "MXOnly-6U-NoLED",
                "MXOnly-6.25U-NoLED",
                "MXOnly-6.5U-NoLED",
                "MXOnly-7U-NoLED",
                "MXOnly-8U-NoLED",
                "MXOnly-9U-NoLED",
                "MXOnly-10U-NoLED",
            ],
            "footprint-nameformat": "MXOnly-{}U-NoLED",
        },
    },
    "Switch_Keyboard": {
        "source": "https://github.com/perigoso/Switch_Keyboard",
        "modules": [],  # not supported yet
    },
}


def get_switch_footprint(
    library_module, footprint_format, footprints, key_size
):
    footprint = f"{footprint_format}".format(key_size)
    if footprint in footprints:
        return f"{library_module}:{footprint}"
    # fallback if footpring not found, add some warning:
    return f"{library_module}:{footprints[0]}"


def handle_key_matrix(keys, **kwargs):
    switch_library = kwargs["switch_library"]
    library_module = kwargs["library_module"]

    module = SUPPORTED_LIBRARIES[switch_library][library_module]
    available_footprints = module["footprints"]
    footprint_format = module["footprint-nameformat"]

    rows = {}
    columns = {}

    for key in keys:
        labels = key["labels"]
        if not labels:
            raise RuntimeError("Key label for matrix position missing")

        row, column = map(int, labels[0].split(","))
        if not row in rows:
            rows[row] = Net(f"ROW{row}")
        if not column in columns:
            columns[column] = Net(f"COL{column}")

        switch_footprint = get_switch_footprint(
            library_module, footprint_format, available_footprints, key["width"]
        )
        k = Part("Switch", "SW_Push", footprint=switch_footprint)
        d = Part("Device", "D", footprint="Diode_SMD:D_SOD-323F")

        rows[row] += d[1]
        columns[column] += k[1]
        _ = k[2] & d[2]


def kle2netlist(layout, output_path, **kwargs):
    additional_search_path = kwargs.get("additional_search_path")
    for path in additional_search_path:
        lib_search_paths[KICAD].append(path)

    switch_library = kwargs.get("switch_library")
    if switch_library not in SUPPORTED_LIBRARIES.keys():
        raise RuntimeError(
            f"Unsupported switch_library argument: {switch_library}"
        )

    library_module = kwargs.get("library_module")
    supported_modules = SUPPORTED_LIBRARIES[switch_library]["modules"]
    if library_module not in supported_modules:
        raise RuntimeError(
            f"Unsupported library_module argument: {library_module}"
        )

    arguments = {
        "switch_library": switch_library,
        "library_module": library_module,
    }
    handle_key_matrix(layout["keys"], **arguments)

    generate_netlist(file_=output_path)


__all__ = ["kle2netlist"]

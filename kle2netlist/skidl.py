from skidl import *


def handle_key_matrix(keys):
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

        k = Part(
            "MX_Alps_Hybrid", "MX-NoLED", footprint="MX_Only:MXOnly-1U-NoLED"
        )
        d = Part("Device", "D", footprint="Diode_SMD:D_SOD-323F")
        rows[row] += d[1]
        columns[column] += k[1]
        _ = k[2] & d[2]


def kle2netlist(layout, output_path, additional_search_path=[]):
    for path in additional_search_path:
        lib_search_paths[KICAD].append(path)

    handle_key_matrix(layout["keys"])
    generate_netlist(file_=output_path)


__all__ = ["kle2netlist"]

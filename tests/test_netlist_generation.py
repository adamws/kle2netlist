import json
import os
import pathlib
import shutil

import pytest
from kle2netlist.skidl import kle2netlist


def compare_files(reference, result):
    f1 = open(reference)
    f2 = open(result)

    f1_line = f1.readline()
    f2_line = f2.readline()

    while f1_line != "" or f2_line != "":
        if not f1_line.startswith("#"):
            assert f1_line == f2_line

        f1_line = f1.readline()
        f2_line = f2.readline()

    f1.close()
    f2.close()


@pytest.mark.parametrize(
    ("layout_id", "switch_library", "switch_footprint"),
    [
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "MX"),
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "Alps"),
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "MX/Alps Hybrid"),
        ("2x2", "perigoso/Switch_Keyboard", "MX"),
        ("2x2", "perigoso/Switch_Keyboard", "Alps"),
        ("2x2", "perigoso/Switch_Keyboard", "MX/Alps Hybrid"),
    ],
)
def test_netlist_generation(
    layout_id, switch_library, switch_footprint, tmpdir, request
):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    layout_filename = layout_id + ".json"
    switch_library_name = switch_library.replace("/", "-")
    switch_footprint_name = switch_footprint.replace("/", "-").replace(" ", "-")
    expected_netlist = (
        f"{layout_id}-{switch_library_name}-{switch_footprint_name}.net"
    )

    if os.path.isdir(test_dir):
        shutil.copy(test_dir + "/" + layout_filename, str(tmpdir))
        shutil.copy(test_dir + "/" + expected_netlist, str(tmpdir))

    with open(tmpdir.join(layout_filename)) as f:
        layout = json.loads(f.read())

    result_netlist_path = str(tmpdir.join("test.net"))

    kle2netlist(
        layout,
        result_netlist_path,
        switch_library=switch_library,
        switch_footprint=switch_footprint,
        additional_search_path=[
            "/usr/share/kicad/library",
        ],
    )

    compare_files(str(tmpdir.join(expected_netlist)), result_netlist_path)

# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import json
import os
import shutil

import jinja2
import pytest

from kle2netlist.skidl import build_circuit, generate_netlist


def assert_netlist(netlist_template, result_file, template_dict):
    with open(netlist_template) as f:
        netlist_template = jinja2.Template(
            f.read(), trim_blocks=True, lstrip_blocks=True
        )

    reference_netlist = netlist_template.render(template_dict)

    result_netlist = open(result_file)

    for line in reference_netlist.splitlines():
        result_line = result_netlist.readline()
        if not line.startswith("#"):
            assert line == result_line.rstrip()

    result_netlist.close()


@pytest.mark.parametrize(
    ("layout_id", "controller_circuit"),
    [
        ("2x2", False),
        ("2x2", True),
        ("iso-enter", False),
        ("empty", True),
    ],
)
def test_netlist_generation(
    layout_id,
    controller_circuit,
    tmpdir,
    request,
):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    layout_filename = f"{layout_id}.json"
    controller_circuit_suffix = "-with-uc" if controller_circuit else ""
    netlist_template = f"{layout_id}{controller_circuit_suffix}.net"

    if os.path.isdir(test_dir):
        shutil.copy(f"{test_dir}/{layout_filename}", str(tmpdir))
        shutil.copy(f"{test_dir}/{netlist_template}", str(tmpdir))

    with open(tmpdir.join(layout_filename)) as f:
        layout = json.loads(f.read())

    result_netlist_path = str(tmpdir.join("test.net"))

    build_circuit(
        layout,
        switch_footprint="PCM_lib1:SW_{:.2f}u",
        stabilizer_footprint="PCM_lib2:ST_{:.2f}u",
        diode_footprint="Diode_SMD:D_SOD-323F",
        controller_circuit=controller_circuit,
    )
    generate_netlist(result_netlist_path)

    template_dict = {
        "switch_footprint_1u": "PCM_lib1:SW_1.00u",
        "switch_footprint_iso_enter": "PCM_lib1:SW_1.00u",  # dedicated ISO enters not used
        "stabilizer_footprint_2u": "PCM_lib2:ST_2.00u",
    }
    assert_netlist(
        str(tmpdir.join(netlist_template)), result_netlist_path, template_dict
    )


@pytest.mark.parametrize(
    ("labels"),
    [
        [None, None],
        [None, "1,2"],
        ["1,x"],
        ["x,1"],
        ["1,"],
        [",1"],
        ["'1,2'"],
    ],
)
def test_layout_with_wrong_labels(labels):
    layout = {
        "keys": [
            {
                "labels": labels,
                "x": 0,
                "y": 0,
                "width": 1,
                "height": 1,
                "width2": 1,
                "height2": 1,
            },
        ]
    }
    with pytest.raises(RuntimeError, match="Key label invalid"):
        build_circuit(
            layout,
            switch_library="ai03-2725/MX_Alps_Hybrid",
            switch_footprint="MX",
            diode_footprint="D_SOD-323F",
            controller_circuit=False,
        )


@pytest.mark.parametrize(
    ("width,expected_key,expected_stabilizer"),
    [
        (2, "2.00u", "2.00u"),
        (2.25, "2.25u", "2.00u"),
        (2.5, "2.50u", "2.00u"),
        (2.75, "2.75u", "2.00u"),
        (3, "3.00u", "3.00u"),
        (3.25, "1.00u", ""),
        (3.5, "1.00u", ""),
        (4, "4.00u", "3.00u"),
        (4.25, "1.00u", ""),
        (5, "1.00u", ""),
        (6, "6.00u", "6.00u"),
        (6.25, "6.25u", "6.25u"),
        (7, "7.00u", "7.00u"),
        (7.5, "1.00u", ""),
        (8, "1.00u", ""),
        (8.5, "1.00u", ""),
        (9, "1.00u", ""),
        (10, "1.00u", ""),
    ],
)
def test_add_stabilizer(width, expected_key, expected_stabilizer, request, tmpdir):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    netlist_template = "key-with-stabilizer.net"
    if os.path.isdir(test_dir):
        shutil.copy(f"{test_dir}/{netlist_template}", str(tmpdir))

    layout = {
        "keys": [
            {
                "labels": ["0,0"],
                "x": 0,
                "y": 0,
                "width": width,
                "height": 1,
                "width2": 1,
                "height2": 1,
            },
        ]
    }

    result_netlist_path = str(tmpdir.join("test.net"))
    build_circuit(
        layout,
        switch_footprint="PCM_lib1:SW_{:.2f}u",
        stabilizer_footprint="PCM_lib2:ST_{:.2f}u",
        diode_footprint="Diode_SMD:D_SOD-323F",
        controller_circuit=False,
    )
    generate_netlist(result_netlist_path)
    template_dict = {
        "switch_footprint": f"PCM_lib1:SW_{expected_key}",
    }
    if expected_stabilizer:
        template_dict["stabilizer_footprint"] = f"PCM_lib2:ST_{expected_stabilizer}"

    assert_netlist(
        str(tmpdir.join(netlist_template)), result_netlist_path, template_dict
    )

import json
import os
import pathlib
import shutil

import jinja2
import pytest
from kle2netlist.skidl import build_circuit, generate_netlist

# reference dicts
REFERENCE_TEMPLATE_DICT = {
    "ai03-2725/MX_Alps_Hybrid": {
        "MX": {"switch_footprint_1u": "MX_Only:MXOnly-1U-NoLED"},
        "Alps": {"switch_footprint_1u": "Alps_Only:ALPS-1U"},
        "MX/Alps Hybrid": {"switch_footprint_1u": "MX_Alps_Hybrid:MX-1U-NoLED"},
    },
    "perigoso/keyswitch-kicad-library": {
        "MX": {
            "switch_footprint_1u": "Switch_Keyboard_Cherry_MX:SW_Cherry_MX_PCB_1.00u",
            "switch_footprint_iso_enter": "Switch_Keyboard_Cherry_MX:SW_Cherry_MX_PCB_ISOEnter",
            "stabilizer_footprint_2u": "Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_2u",
        },
        "Alps": {
            "switch_footprint_1u": "Switch_Keyboard_Alps_Matias:SW_Alps_Matias_1.00u"
        },
        "MX/Alps Hybrid": {
            "switch_footprint_1u": "Switch_Keyboard_Hybrid:SW_Hybrid_Cherry_MX_Alps_1.00u"
        },
    },
}


def assert_netlist(netlist_template, result_file, template_dict):
    with open(netlist_template) as f:
        netlist_template = jinja2.Template(f.read())

    reference_netlist = netlist_template.render(template_dict)

    result_netlist = open(result_file)

    for line in reference_netlist.splitlines():
        result_line = result_netlist.readline()
        if not line.startswith("#"):
            assert line == result_line.rstrip()

    result_netlist.close()


@pytest.mark.parametrize(
    ("layout_id", "switch_library", "switch_footprint", "controller_circuit"),
    [
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "MX", False),
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "Alps", False),
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "MX/Alps Hybrid", False),
        ("2x2", "perigoso/keyswitch-kicad-library", "MX", False),
        ("2x2", "perigoso/keyswitch-kicad-library", "Alps", False),
        ("2x2", "perigoso/keyswitch-kicad-library", "MX/Alps Hybrid", False),
        ("iso-enter", "perigoso/keyswitch-kicad-library", "MX", False),
        ("empty", "ai03-2725/MX_Alps_Hybrid", "MX", True),
        ("empty", "perigoso/keyswitch-kicad-library", "MX", True),
        ("2x2", "ai03-2725/MX_Alps_Hybrid", "MX", True),
        ("2x2", "perigoso/keyswitch-kicad-library", "MX", True),
    ],
)
def test_netlist_generation(
    layout_id,
    switch_library,
    switch_footprint,
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
        switch_library=switch_library,
        switch_footprint=switch_footprint,
        controller_circuit=controller_circuit,
    )
    generate_netlist(result_netlist_path)

    template_dict = REFERENCE_TEMPLATE_DICT[switch_library][switch_footprint]
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
        ["1, 2"],
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
            controller_circuit=False,
        )

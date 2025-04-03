# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import os
import shutil

import jinja2
import pytest
from typer.testing import CliRunner

from kle2netlist.__main__ import app
from kle2netlist.netlist import build_circuit, generate_netlist

LAYOUT_RUNTIME_ERROR = (
    "Layout from '.*' is not convertable to matrix annotated keyboard"
)
LABEL_VALUE_ERROR = "No numeric part for row or column found in"

runner = CliRunner()


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


@pytest.fixture
def file_isolation(tmpdir, request):
    def _copy_files(layout_filename, netlist_template) -> None:
        filename = request.module.__file__
        test_dir, _ = os.path.splitext(filename)

        if os.path.isdir(test_dir):
            shutil.copy(f"{test_dir}/{layout_filename}", tmpdir)
            shutil.copy(f"{test_dir}/{netlist_template}", tmpdir)

    return _copy_files


@pytest.mark.parametrize(
    (
        "layout_filename",
        "netlist_template",
        "circuits",
        "row_column_pin_order",
    ),
    [
        # fmt: off
        ("2x2.json", "2x2.net", None, None),
        ("2x2.json", "2x2-with-uc.net", ["atmega32u4", "usb"], None),
        ("2x2.json", "2x2-with-uc-custom-order.net", ["atmega32u4", "usb"], ["PD0", "PD1", "PF0", "PF1"]),
        ("2x2-with-alternative-layout.json", "2x2-with-alternative-layout.net", None, None),
        ("iso-enter.json", "iso-enter.net", None, None),
        ("empty.json", "empty-with-uc.net", ["atmega32u4", "usb"], None),
        # fmt: on
    ],
)
class TestNetlistGeneration:
    TEMPLATE_DICT = {
        "switch_footprint_1u": "PCM_lib1:SW_1.00u",
        "switch_footprint_2u": "PCM_lib1:SW_2.00u",
        "switch_footprint_iso_enter": "PCM_lib1:SW_1.00u",  # dedicated ISO enters not used
        "stabilizer_footprint_2u": "PCM_lib2:ST_2.00u",
    }

    def test_api(
        self,
        layout_filename,
        netlist_template,
        circuits,
        row_column_pin_order,
        file_isolation,
        tmpdir,
    ) -> None:
        file_isolation(layout_filename, netlist_template)
        result_netlist_path = tmpdir.join("test.net")

        circuit = build_circuit(
            tmpdir.join(layout_filename),
            switch_footprint="PCM_lib1:SW_{:.2f}u",
            stabilizer_footprint="PCM_lib2:ST_{:.2f}u",
            diode_footprint="Diode_SMD:D_SOD-323F",
            controller_circuit=circuits[0] if circuits else None,
            extra_circuits=circuits[1:] if circuits and len(circuits) > 1 else None,
            row_column_pin_order=row_column_pin_order,
        )
        generate_netlist(circuit, result_netlist_path)

        assert_netlist(
            tmpdir.join(netlist_template), result_netlist_path, self.TEMPLATE_DICT
        )

    def test_cli(
        self,
        layout_filename,
        netlist_template,
        circuits,
        row_column_pin_order,
        file_isolation,
        tmpdir,
    ) -> None:
        file_isolation(layout_filename, netlist_template)
        result_netlist_path = tmpdir.join("test.net")

        # fmt: off
        args = [
            "--layout", tmpdir.join(layout_filename),
            "--output", result_netlist_path,
            "--switch-footprint", "PCM_lib1:SW_{:.2f}u",
            "--stabilizer-footprint", "PCM_lib2:ST_{:.2f}u",
            "--diode-footprint", "Diode_SMD:D_SOD-323F",
        ]
        if circuits and circuits[0]:
            args.append("--controller-circuit")
            args.append(circuits[0])
        if circuits and len(circuits) > 1:
            for c in circuits[1:]:
                args.append("--extra-circuits")
                args.append(c)
        # fmt: on
        if row_column_pin_order:
            args.append("--row-column-pin-order")
            args.append(",".join(row_column_pin_order))

        args_str = " ".join([f"{a}" for a in args])
        result = runner.invoke(app, args)
        assert result.exit_code == 0

        assert_netlist(
            tmpdir.join(netlist_template), result_netlist_path, self.TEMPLATE_DICT
        )


def test_no_fstring_footprint(tmpdir, request):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    layout_id = "2x2"

    layout_filename = f"{layout_id}.json"
    netlist_template = f"{layout_id}.net"

    if os.path.isdir(test_dir):
        shutil.copy(f"{test_dir}/{layout_filename}", str(tmpdir))
        shutil.copy(f"{test_dir}/{netlist_template}", str(tmpdir))

    result_netlist_path = str(tmpdir.join("test.net"))
    circuit = build_circuit(
        tmpdir.join(layout_filename),
        switch_footprint="PCM_lib1:SW",
        stabilizer_footprint="",
        diode_footprint="Diode_SMD:D_SOD-323F",
    )
    generate_netlist(circuit, result_netlist_path)

    template_dict = {
        "switch_footprint_1u": "PCM_lib1:SW",
    }
    assert_netlist(
        str(tmpdir.join(netlist_template)), result_netlist_path, template_dict
    )


@pytest.mark.parametrize(
    ("layout", "expected_exception", "exception_match"),
    [
        ('[[{"a": 0}, ""]]', RuntimeError, LAYOUT_RUNTIME_ERROR),
        ('[[{"a": 5}, "1,2"]]', RuntimeError, LAYOUT_RUNTIME_ERROR),
        ('[["1,x"]]', ValueError, LABEL_VALUE_ERROR),
        ('[["x,1"]]', ValueError, LABEL_VALUE_ERROR),
        ('[["1,"]]', ValueError, LABEL_VALUE_ERROR),
        ('[[",1"]]', ValueError, LABEL_VALUE_ERROR),
    ],
)
def test_wrongly_annotated_layouts(layout, expected_exception, exception_match, tmpdir):
    layout_file = tmpdir.join("layout.json")
    with open(layout_file, "w") as f:
        f.write(layout)

    with pytest.raises(expected_exception, match=exception_match):
        build_circuit(
            layout_file,
            switch_footprint="PCM_lib1:SW_{:.2f}u",
            stabilizer_footprint="PCM_lib2:ST_{:.2f}u",
            diode_footprint="Diode_SMD:D_SOD-323F",
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

    layout = f'[[{{"w": {width}}}, "0,0"]]'
    layout_file = tmpdir.join("layout.json")
    with open(layout_file, "w") as f:
        f.write(layout)

    result_netlist_path = str(tmpdir.join("test.net"))
    circuit = build_circuit(
        layout_file,
        switch_footprint="PCM_lib1:SW_{:.2f}u",
        stabilizer_footprint="PCM_lib2:ST_{:.2f}u",
        diode_footprint="Diode_SMD:D_SOD-323F",
    )
    generate_netlist(circuit, result_netlist_path)
    template_dict = {
        "switch_footprint": f"PCM_lib1:SW_{expected_key}",
    }
    if expected_stabilizer:
        template_dict["stabilizer_footprint"] = f"PCM_lib2:ST_{expected_stabilizer}"

    assert_netlist(
        str(tmpdir.join(netlist_template)), result_netlist_path, template_dict
    )

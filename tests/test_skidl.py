import json
import os
import pathlib

import pytest
from kle2netlist.skidl import kle2netlist

TWO_KEYS_LAYOUT = """{"meta":{"author":"","backcolor":"#eeeeee","background":null,"name":"","notes":"","radii":"","switchBrand":"","switchMount":"","switchType":""},"keys":[{"color":"#cccccc","labels":["0,0"],"textColor":[],"textSize":[],"default":{"textColor":"#000000","textSize":3},"x":0,"y":0,"width":2.75,"height":1,"x2":0,"y2":0,"width2":1,"height2":1,"rotation_x":0,"rotation_y":0,"rotation_angle":0,"decal":false,"ghost":false,"stepped":false,"nub":false,"profile":"","sm":"","sb":"","st":""},{"color":"#cccccc","labels":["0,1"],"textColor":[],"textSize":[],"default":{"textColor":"#000000","textSize":3},"x":1,"y":0,"width":1,"height":1,"x2":0,"y2":0,"width2":1,"height2":1,"rotation_x":0,"rotation_y":0,"rotation_angle":0,"decal":false,"ghost":false,"stepped":false,"nub":false,"profile":"","sm":"","sb":"","st":""}]}"""


@pytest.mark.parametrize(
    ("layout", "switch_library", "switch_footprint"),
    [
        (TWO_KEYS_LAYOUT, "ai03-2725/MX_Alps_Hybrid", "MX"),
        (TWO_KEYS_LAYOUT, "ai03-2725/MX_Alps_Hybrid", "Alps"),
        (TWO_KEYS_LAYOUT, "ai03-2725/MX_Alps_Hybrid", "MX/Alps Hybrid"),
        (TWO_KEYS_LAYOUT, "perigoso/Switch_Keyboard", "MX"),
        (TWO_KEYS_LAYOUT, "perigoso/Switch_Keyboard", "Alps"),
        (TWO_KEYS_LAYOUT, "perigoso/Switch_Keyboard", "MX/Alps Hybrid"),
    ],
)
def test_netlist_generation(layout, switch_library, switch_footprint, tmpdir):
    os.chdir(tmpdir)
    f = tmpdir.join("test.net")

    kle2netlist(
        json.loads(layout),
        str(f.realpath()),
        switch_library=switch_library,
        switch_footprint=switch_footprint,
        additional_search_path=[
            "/usr/share/kicad/library",
        ],
    )

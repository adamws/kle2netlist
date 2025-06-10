# SPDX-FileCopyrightText: 2021-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import importlib.resources
import sys
from typing import List, Optional

import skidl

skidl.set_default_tool(skidl.KICAD8)


def set_skidl_search_path(
    additional_search_path: Optional[List[str]] = None,
) -> None:
    if additional_search_path:
        for path in additional_search_path:
            skidl.lib_search_paths[skidl.KICAD].append(str(path))

    # try using bundled symbols as fallback:
    if sys.version_info[1] >= 10:
        with importlib.resources.path("kle2netlist", "data") as p:
            default_search_path = p.joinpath("kicad-symbols")
    else:
        # for python <3.9 you can't use directory as resource:
        with importlib.resources.path("kle2netlist", "skidl.py") as p:
            default_search_path = p.parent.joinpath("data/kicad-symbols")
    skidl.lib_search_paths[skidl.KICAD8].append(str(default_search_path))

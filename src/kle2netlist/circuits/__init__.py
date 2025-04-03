# SPDX-FileCopyrightText: 2024-present adamws <adamws@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import importlib
import pkgutil

from skidl import Net

# Dictionary to hold available circuits
_circuit_modules = {}

# Automatically discover and register all circuit modules
for _, mod_name, _ in pkgutil.iter_modules(__path__):
    _circuit_modules[mod_name] = f"kle2netlist.circuits.{mod_name}"


def get_circuit(name):
    """Dynamically import and return the circuit module."""
    if name not in _circuit_modules:
        raise ValueError(f"Unknown circuit: {name}")

    return importlib.import_module(_circuit_modules[name])

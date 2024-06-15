# kle2netlist

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---     | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| CI/CD   | [![CI - Main](https://github.com/adamws/kle2netlist/actions/workflows/build.yml/badge.svg)](https://github.com/adamws/kle2netlist/actions/workflows/build.yml) [![Coverage Status](https://coveralls.io/repos/github/adamws/kle2netlist/badge.svg?branch=master)](https://coveralls.io/github/adamws/kle2netlist?branch=master)                                                                                                                                                                                                                                                                                    |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/kle2netlist.svg)](https://pypi.org/project/kle2netlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Meta    | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

-----

**KiCad netlist generator for mechanical keyboards**

## Installation

```
pip install kle2netlist
```

## Usage

```
$ kle2netlist --help

Usage: kle2netlist [OPTIONS]

Generates KiCad netlist for a given keyboard layout json file.

Options
--layout                Path to kle layout file [default: None] [required]
--output                Output netlist file [default: keyboard.net]
--switch-footprint      Switch footprint f-string [default: PCM_Switch_Keyboard_Cherry_MX:SW_Cherry_MX_PCB_{:.2f}u]
--stabilizer-footprint  Stabilizer footprint f-string, optional [default: PCM_Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{:.2f}u]
--diode-footprint       Diode footprint [default: Diode_SMD:D_SOD-123F]
--lib-path              Path to symbol library [default: None]
--controller-circuit    Add microcontroller circuitry [default: none]
--version               Prints the version of the kle2netlist package.
--help                  Show this message and exit.
```

### Controller circuit templates

<table>
    <tr>
        <td style="width:10%" align="center"><b>Name</b></td>
        <td align="center"><b>Description</b></td>
        <td style="width:50%"align="center"><b>Layout</b></td>
    </tr>
    <tr>
        <td>atmega32u4_au_v1</td>
        <td>[todo]</td>
        <td><img src="kicad-templates/atmega32u4-au-v1/atmega32u4-au-v1.svg"/></td>
    </tr>
</table>

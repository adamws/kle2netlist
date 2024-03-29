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
--layout                    Path to kle layout file [default: None] [required]
--output-dir                Output directory, created if not existing [default: .]
--name                      Netlist name without file extension [default: keyboard]
--switch-footprint -swf     Switch footprint f-string [default: PCM_Switch_Keyboard_Cherry_MX:SW_Cherry_MX_PCB_{:.2f}u]
--stabilizer-footprint -stf Stabilizer footprint [default: PCM_Mounting_Keyboard_Stabilizer:Stabilizer_Cherry_MX_{:.2f}u]
--diode-footprint -df       Diode footprint [default: Diode_SMD:D_SOD-123F]
--lib-path -l               Path to symbol library [default: None]
--controller-circuit        Add ATmega32U4-AU minimal circuitry
--no-xml                    Skip xml netlist generation
--version -v                Prints the version of the kle2netlist package.
--help                      Show this message and exit.
```

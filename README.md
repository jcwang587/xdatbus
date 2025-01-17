<p class="center-content"> 
  <img src="https://raw.githubusercontent.com/jcwang587/xdatbus/main/docs/logo.png" alt=""/>
</p>

# xdatbus

[![Build](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml/badge.svg)](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml)
[![Release](https://img.shields.io/github/v/release/jcwang587/xdatbus)](https://github.com/jcwang587/xdatbus/releases)
  [![PyPI Downloads](https://static.pepy.tech/badge/xdatbus)](https://pepy.tech/projects/xdatbus)
[![codecov](https://codecov.io/gh/jcwang587/xdatbus/branch/main/graph/badge.svg?token=V27VIJZDAE)](https://codecov.io/gh/jcwang587/xdatbus)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Xdatbus is a Python package designed specifically for Vienna Ab-initio Simulation Package (VASP) users conducting
ab-initio molecular dynamics (AIMD) simulations, as well as biased MD simulations. The name of the package is derived 
from the MD trajectory file (XDATCAR) generated by VASP. The documentation for 
the package can be accessed [here](https://xdatbus.readthedocs.io/en/latest/), and a collection of 
Jupyter Notebook [tutorial](https://github.com/jcwang587/xdatbus/tree/main/examples) is also available.

## Installation

Make sure you have a Python interpreter, preferably version 3.10 or higher. Then, you can simply install xdatbus from
PyPI using `pip`:

```bash
pip install xdatbus
```

If you'd like to use the latest unreleased version on the main branch, you can install it directly from GitHub:

```bash
pip install git+https://github.com/jcwang587/xdatbus
```

The package is also available from conda-based installation. It is generally recommended you first create a separate
environment, then you can install via the xdatbus channel on Anaconda cloud:

```bash
conda install --channel xdatbus xdatbus
```

If you plan to use PLUMED to analyze enhanced sampling AIMD results, you can also install the conda version of PLUMED
together:

```bash
conda install -c xdatbus -c conda-forge xdatbus plumed
```

## Get Started

This is a brief example demonstrating how to use the basic function of xdatbus to aggregate multiple xdatcar files into
a single file and unwrap the coordinates into an `.xyz` file.

As is the case when you have submitted a continuous AIMD job, it is likely that you would have subfolders for each 
submission. `XDATCAR` files can be first gathered in a separate directory by:

```bash
$ mkdir xdc_files && for i in {01..10}; do cp RUN$i/XDATCAR xdc_files/XDATCAR_$i; done
```

Then, try aggregating and unwrapping the coordinate data from the `XDATCAR` files:

```python
import os
from xdatbus import xdc_aggregate, xdc_unwrap

xdc_dir = "./xdc_files"
xdb_dir = os.path.dirname(xdc_dir)
xdb_path = os.path.join(xdb_dir, "XDATBUS")
xyz_path = os.path.join(xdb_dir, "XDATBUS_unwrap.xyz")

xdc_aggregate(xdc_dir=xdc_dir, output_dir=xdb_dir)
xdc_unwrap(xdc_path=xdb_path, output_path=xyz_path)
```

There are also entry points included with the installation for the Command Line Interface (CLI) to perform similar
tasks:

```bash
$ xdc_aggregate --xdc_dir ./xdc_files --output_dir ./
```

```bash
$ xdc_unwrap --xdc_path ./XDATBUS --output_path ./XDATBUS_unwrap.xyz
```

## Major Changelog
`0.3.0` Enabled the functions for locating minima and running NEB in 2D FES.

`0.2.5` Enabled CLI through the `rich` package.

`0.2.0` Added a function to generate [extxyz](https://github.com/libAtoms/extxyz)-formatted data for training machine 
learning interatomic potentials.

<p class="center-content"> 
  <img src="https://raw.githubusercontent.com/jcwang587/xdatbus/main/docs/logo.png" alt=""/>
</p>

# xdatbus

[![Build](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml/badge.svg)](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml)
[![PyPI](https://img.shields.io/pypi/v/xdatbus?logo=pypi&logoColor=white&color=0073B7)](https://pypi.org/project/xdatbus/)
[![Conda](https://img.shields.io/conda/v/xdatbus/xdatbus?logo=anaconda&logoColor=white&label=conda&color=43B02A)](https://anaconda.org/xdatbus/xdatbus)
[![codecov](https://codecov.io/gh/jcwang587/xdatbus/branch/main/graph/badge.svg?token=V27VIJZDAE)](https://codecov.io/gh/jcwang587/xdatbus)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Xdatbus is a Python library designed specifically for Vienna Ab-initio Simulation Package (VASP) users conducting
ab-initio molecular dynamics (AIMD) simulations, as well as biased MD simulations. The name of the package is derived
from XDATCAR, which represents the combined AIMD trajectories generated by VASP. Documentation for the package can be
accessed [here](https://xdatbus.readthedocs.io/en/latest/) and the Jupyter
Notebook [tutorial](https://github.com/jcwang587/xdatbus/tree/main/examples) is also available.

## Installation

Make sure you have a Python interpreter, preferably version 3.10 or higher. Then, you can simply install xdatbus from
PyPI using `pip`:

```bash
pip install xdatbus
```

If you'd like to use the latest unreleased version on the main branch, you can install it directly from GitHub:

```bash
pip install -U git+https://github.com/jcwang587/xdatbus
```

The package is also availabe from conda-based installation. It is generally recommended you first create a separate
environment, then you can install via the xdatbus channel on Anaconda cloud:

```bash
conda install --channel xdatbus xdatbus
```

If you plan to use PLUMED to analyze biased MD sampling results, you can also install the conda version of PLUMED
together:

```bash
conda install -c xdatbus -c conda-forge xdatbus plumed
```


## Get Started

This is a brief example demonstrating how to use the basic function of xdatbus to aggregate multiple xdatcar files into
one and unwrap the coordinates into an .xyz file:

```python
import os
from xdatbus import xdc_aggregate, xdc_unwrap

xdc_dir = "./xdatcar"
xdb_path = os.path.dirname(xdc_dir)

xdc_aggregate(xdc_dir=xdc_dir, output_path=xdb_path)
xdc_unwrap(xdc_path=xdb_path)
```

There is also entry points included with the installation for the command line interface (CLI) to perform the same tasks:

```bash
$ xdc_aggregate --xdc_dir ./xdatcar --output_path ./
$ thermal_report --osz_dir ./oszicar --output_path ./
```

## Major Changelog

`0.2.0` Implemented the preparation of training data for [MACE](https://github.com/ACEsuit/mace) machine learning
interatomic potentials.

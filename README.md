<p align="center"> 
<img src="https://raw.githubusercontent.com/jcwang587/xdatbus/main/docs/logo.png"/>
</p>

# xdatbus

[![Build](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml/badge.svg)](https://github.com/jcwang587/xdatbus/actions/workflows/build.yml)
![Conda](https://img.shields.io/conda/v/xdatbus/xdatbus?logo=anaconda&label=conda&color=dark%20green)
[![codecov](https://codecov.io/gh/jcwang587/xdatbus/branch/main/graph/badge.svg?token=V27VIJZDAE)](https://codecov.io/gh/jcwang587/xdatbus)

**xdatbus** is a Python library designed specifically for VASP users engaged in research on ab-initio MD simulations, as well as biased MD simulations. The primary file addressed by the package is the XDATCAR, a trajectories file generated by the Vienna Ab-initio Simulation Package (VASP). The package documentation can be accessed [here](https://xdatbus.readthedocs.io/en/latest/) and the Jupyter Notebook [tutorial](https://github.com/jcwang587/xdatbus/tree/main/examples) is also available.


## Installation

Make sure you have a Python interpreter, preferably version 3.10 or higher. Then, you can simply install xdatbus from pypi using `pip`:

```bash
pip install xdatbus
```

If you'd like to use the latest unreleased version on the main branch, you can install it directly from GitHub:

```bash
pip install -U git+https://https://github.com/jcwang587/xdatbus
```
The package is also availabe from conda-based installation. It is generally recommended you first create a separate environment, then you can install xdatbus via conda as well via the xdatbus channel on Anaconda cloud:
```bash
conda install --channel xdatbus xdatbus
```

If you plan to use PLUMED to analyze biased MD sampling results, you can also install the conda version of PLUMED together:
```bash
conda install -c xdatbus -c conda-forge xdatbus plumed
```

## Get Started

This is a brief example demonstrating how to use the basic function of xdatbus to aggregate multiple xdatcar files into one and unwrap the coordinates into an .xyz file:

```python
import os
from xdatbus import xdc_aggregate, xdc_unwrap

xdc_dir = "./data"
xdb_path = os.path.dirname(xdc_dir)

xdc_aggregate(xdc_dir=xdc_dir, output_path=xdb_path)
xdc_unwrap(xdc_path=xdb_path)
```

## Update log
`0.0.6` first upload for test

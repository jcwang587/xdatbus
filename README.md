# xdatbus

[![Build](https://github.com/jcwang587/xdatbus/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jcwang587/xdatbus/actions/workflows/python-publish.yml)
[![codecov](https://codecov.io/gh/jcwang587/xdatbus/branch/main/graph/badge.svg?token=V27VIJZDAE)](https://codecov.io/gh/jcwang587/xdatbus)

**xdatbus** is a Python library specifically tailored for VASP users engaged in research on ab-initio MD simulations, as well as biased MD simulations. The primary file addressed by the package is the XDATCAR, a trajectories file generated by the Vienna Ab-initio Simulation Package (VASP). The package documentation can be accessed [here](https://xdatbus.readthedocs.io/en/latest/) and the Jupyter Notebook [tutorial](https://github.com/jcwang587/xdatbus/tree/main/examples) is also available.


## Installation

Make sure you have a Python interpreter, preferably version 3.10 or higher:

```bash
$ python --version
Python 3.11.4
```

Then, you can simply install `xdatbus` from pypi using `pip`:

```bash
$ pip install xdatbus
```

If you'd like to use the latest unreleased version on the main branch, you can install it directly from GitHub:

```bash
$ pip install -U git+https://https://github.com/jcwang587/xdatbus
```


## Get Started

This is a brief example demonstrating how to use the basic function of `xdatbus` to aggregate multiple xdatcar files into one and unwrap the coordinates into an .xyz file.:

```python
import os
from xdatbus import f01_aggregate, f02_unwrap

aimd_path = "./data"
output_path = os.path.dirname(aimd_path)

f01_aggregate(aimd_path=aimd_path, output_path=output_path)
f02_unwrap(xdatcar_path=output_path)
```

## Update log
`0.0.6` first upload for test

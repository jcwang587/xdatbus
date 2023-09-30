# XDATBUS

[![Build](https://github.com/jcwang587/xdatbus/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jcwang587/xdatbus/actions/workflows/python-publish.yml)
[![codecov](https://codecov.io/gh/jcwang587/xdatbus/branch/main/graph/badge.svg?token=V27VIJZDAE)](https://codecov.io/gh/jcwang587/xdatbus)

A Python package to analyze XDATCAR files generated from VASP output files. XDATBUS is an enhanced toolkit used to assist in the analysis of XDATCAR files. It currently includes three main functions: 1. Unfolding and merging paths, 2. Fixing specific atoms, 3. Crystal cell expansion, and 4. Real-time CV-structure transfer based on Metadynamics. The XDATCAR python package documentation is available at [documentation](https://github.com/jcwang587/xdatbus) and a Jupyter Notebook tutorial for the API is available [here](https://github.com/jcwang587/xdatbus).



## Installation


Make sure you have a Python interpreter newer than version 3.8:


```bash
❯ python --version
Python 3.8.0
```

Then, you can simply install `xdatbus` from pypi using `pip`:


```bash
pip install xdatbus
```

or

```bash
pip install --upgrade xdatbus
```



## Motivation

The main goal of this project is to provide a tool to efficiently do the analysis of Ab-inito molecular dynamics results from VASP. Under most cases, we care about some certain atoms for MD simulation, while in a framework of other atoms which are supposed to be "fixed". For better visualization, we hope these atoms could be fixed but not vibrating. By applying pymatgen and ASE packages.



## Get Started

The main goal of this project is to provide a tool to efficiently do the analysis of Ab-inito molecular dynamics results from VASP. Under most cases, we care about some certain atoms for MD simulation, while in a framework of other atoms which are supposed to be "fixed". For better visualization, we hope these atoms could be fixed but not vibrating. By applying pymatgen and ASE packages.



## Update log
`0.0.6` first upload for test

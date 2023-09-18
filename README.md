# XDATBUS

[![pytest](https://github.com/olivecha/guitarsounds/actions/workflows/python-app.yml/badge.svg)](https://github.com/olivecha/guitarsounds/actions/workflows/python-app.yml) 

A python package to analyze XDATCAR files generated from VASP output files. XDATBUS is an enhanced toolkit used to assist in the analysis of XDATCAR files. It currently includes three main functions: 1. Unfolding and merging paths, 2. Fixing specific atoms, 3. Crystal cell expansion, and 4. Real-time CV-structure transfer based on Metadynamics. The XDATCAR python package documentation is available at [documentation](https://olivecha.github.io/guitarsounds/guitarsounds.html) and a Jupyter Notebook tutorial for the API is available [here](https://github.com/olivecha/guitarsounds/blob/JOSS-Paper/docs/API_Tutorial.ipynb).

## Motivation

The main goal of this project is to provide a tool to efficiently do the analysis of Ab-inito molecular dynamics results from VASP. Under most cases, we care about some certain atoms for MD simulation, while in a framework of other atoms which are supposed to be "fixed". For better visualization, we hope these atoms could be fixed but not vibrating. By applying pymatgen and ASE packages.
analyse sound data from research projects in musical instrument design. While sound analysis packages already exist, they are more directed to feature extraction for machine learning purposes. Additionally, some features of interest, like time dependent decay, onset shape and fourier transform peaks distribution are not computable trivially or accurately with existing tools. The current release of the guitarsounds package contains usual and advanced digital signal processing tools applied to the analysis of transient harmonic sounds with easy figure generation through `matplotlib`. To allow the package functionalities to be used rapidly without learning the API, a graphic user interface is available based on jupyter lab widgets.

## Update log
`0.0.6` first upload for test
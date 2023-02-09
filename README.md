# XDATBUS

[![pytest](https://github.com/olivecha/guitarsounds/actions/workflows/python-app.yml/badge.svg)](https://github.com/olivecha/guitarsounds/actions/workflows/python-app.yml) 

A python package to analyse guitar sounds. Developed as a lutherie research analysis tool with the [Bruand Lutherie School](https://bruand.com/). 
The guitarsound python package documentation is available at [documentation](https://olivecha.github.io/guitarsounds/guitarsounds.html) and a Jupyter Notebook tutorial for the API is available [here](https://github.com/olivecha/guitarsounds/blob/JOSS-Paper/docs/API_Tutorial.ipynb).

## Motivation

The main goal of this project is to provide a tool to efficiently analyse sound data from research projects in musical instrument design. While sound analysis packages already exist, they are more directed to feature extraction for machine learning purposes. Additionally, some features of interest, like time dependent decay, onset shape and fourier transform peaks distribution are not computable trivially or accurately with existing tools. The current release of the guitarsounds package contains usual and advanced digital signal processing tools applied to the analysis of transient harmonic sounds with easy figure generation through `matplotlib`. To allow the package functionalities to be used rapidly without learning the API, a graphic user interface is available based on jupyter lab widgets.

import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.0.9'
DESCRIPTION = 'A python package to analyze XDATCAR files generated from VASP'
LONG_DESCRIPTION = 'just for test'

setup(
    name="xdatbus",
    version=VERSION,
    author="Jiacheng Wang",
    author_email="jiachengwang@umass.edu",
    maintainer="Jiacheng Wang",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'vasp', 'xdatcar', 'aimd'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        "Operating System :: OS Independent",
    ]
)

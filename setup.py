import codecs
import os
from setuptools import setup, find_packages


def find_repo_root(start_dir):
    """Find the root directory of the repository."""
    current_dir = start_dir
    while True:
        # Check if current_dir is the repository root
        if os.path.isdir(os.path.join(current_dir, 'xdatbus')):
            return current_dir
        # Check if we've reached the root of the filesystem
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # If so, the repository root wasn't found
            raise FileNotFoundError("Repository root not found")
        # Otherwise, move up the directory hierarchy
        current_dir = parent_dir


# Get the directory containing setup.py
setup_dir = os.path.abspath(os.path.dirname(__file__))

# Find the repository root
repo_root = find_repo_root(setup_dir)

# Construct the paths to README.md and requirements.txt
readme_path = os.path.join(repo_root, "README.md")
requirements_path = os.path.join(repo_root, 'requirements.txt')
requirements_vis_path = os.path.join(repo_root, 'requirements_vis.txt')

with codecs.open(readme_path, encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open(requirements_path) as f:
    required = f.read().splitlines()

with open(requirements_vis_path) as f:
    vis_required = f.read().splitlines()

# These are the optional requirements
package_data = {
    'xdatbus': ['resources/*.blend'],
}

extras_require = {
    'vis': vis_required,
}

DESCRIPTION = 'A python package to analyze XDATCAR files generated from VASP'
LONG_DESCRIPTION = 'A python package to analyze XDATCAR files generated from VASP'

setup(
    name="xdatbus",
    version="0.0.118",
    author="Jiacheng Wang",
    author_email="jiachengwang@umass.edu",
    maintainer="Jiacheng Wang",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data=package_data,
    install_requires=required,
    extras_require=extras_require,
    keywords=['python', 'vasp', 'xdatcar', 'aimd'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'xdc_aggregate = xdatbus.f01_xdc_aggregate:main',
        ],
    }
)

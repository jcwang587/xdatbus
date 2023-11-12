# Configuration file for the Sphinx documentation builder.

# -- Project information

import os
impor toml
import setuptools
import subprocess


# Function to extract project metadata from pyproject.toml
def get_project_metadata():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    pyproject_path = os.path.join(project_dir, 'pyproject.toml')

    with open(pyproject_path, 'r') as pyproject_file:
        pyproject_data = toml.load(pyproject_file)

    # Extract metadata from pyproject.toml (assuming Poetry is used)
    metadata = pyproject_data['tool']['poetry']

    return metadata, project_dir


# Get project metadata
metadata, repo_dir = get_project_metadata()

# -- Project information

project = metadata['name']
copyright = f"2023, {metadata['author']}"
author = metadata['author']
release = metadata['version']
version = '.'.join(release.split('.')[:2])

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'autoapi.extension'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']
templates_path = ['_templates']

# -- autoapi configuration

autoapi_dirs = os.path.join(repo_dir, 'xdatbus')
autoapi_add_toctree_entry = True
autoapi_type = 'python'
autoapi_keep_files = True
autoapi_root = 'api_reference'

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output

epub_show_urls = 'footnote'

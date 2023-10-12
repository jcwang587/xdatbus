# Configuration file for the Sphinx documentation builder.

# -- Project information

import setuptools

# Function to extract project metadata from setup.py
def get_project_metadata():
    setup_args = {}
    setuptools.setup = lambda *args, **kwargs: setup_args.update(kwargs)
    exec(open('setup.py').read())
    return setup_args

# Get project metadata
metadata = get_project_metadata()

# -- Project information

project = metadata['name']
copyright = f"2023, {metadata['author']}"
author = metadata['author']

release = metadata['version']
# Assuming version is in the format 'major.minor.patch'
version = '.'.join(release.split('.')[:2])

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Configuration file for the Sphinx documentation builder.

# -- Project information

import os
import setuptools
import subprocess

# Function to extract project metadata from setup.py
def get_project_metadata():
    setup_args = {}
    original_setup = setuptools.setup  # Store the original function
    
    # Replace setuptools.setup with a function to capture arguments
    setuptools.setup = lambda *args, **kwargs: setup_args.update(kwargs)
    
    setup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    setup_path = os.path.join(setup_dir, 'setup.py')
    
    # Using a try-finally block to ensure original setup is restored
    try:
        os.chdir(setup_dir)
        exec(open(setup_path).read())
    finally:
        setuptools.setup = original_setup  # Restore the original function
    
    return setup_args, setup_dir

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

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output

epub_show_urls = 'footnote'

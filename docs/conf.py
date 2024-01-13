# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
from linecache import getline
from os.path import abspath
from re import search
from sys import path

path.insert(0, abspath('..'))


# -- Project information -----------------------------------------------------

project = 'enumagic'
copyright = '2020-2024, ObserverOfTime'
author = 'ObserverOfTime'

# The full version, including alpha/beta/rc tags
release = search("'(.+)'", getline('enumagic/__init__.py', 25)).group(1)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx
# (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match
# files and directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.directory']

# The master document.
master_doc = 'index'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = False

# Autodoc settings
autodoc_default_options = {
    'member-order': 'groupwise',
    'show-inheritance': None,
    'special-members': None,
    'undoc-members': None,
    'exclude-members': ','.join((
        '__new__',
        '__dict__',
        '__init__',
        '__module__',
        '__weakref__',
        '__annotations__',
        '__init_subclass__',
    )),
}
autodoc_inherit_docstrings = True
always_document_param_types = True

# Intersphinx settings
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.9/', None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
# See the documentation for a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [
    __import__(html_theme).get_html_theme_path()
]
html_theme_options = {
    'display_version': True,
    'collapse_navigation': True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version

sys.path.insert(0, os.path.abspath(".."))

project = "NextGenVol IBKR Reports"
copyright = "2023, Weston Platter"
author = "Weston Platter"

try:
    release = pkg_version("ngv_reports_ibkr")
except PackageNotFoundError:  # not installed, eg. a bare `sphinx-build` checkout
    release = "0.0.0"
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = []

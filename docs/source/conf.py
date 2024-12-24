# ThermalPrinter documentation build configuration file, created by
# sphinx-quickstart on Tue Sep 27 11:49:38 2016.

# Lets prevent misses, and import the module to get the proper version.
# So that the version in only defined once across the whole code base:
#   src/thermalprinter/__init__.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import thermalprinter

# -- General configuration ------------------------------------------------

extensions = [
    "enum_tools.autoenum",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_new_tab_link",
]
new_tab_link_show_external_link_icon = True
source_suffix = {".rst": "restructuredtext"}
extlinks = {
    "contributor": ("https://github.com/BoboTiG/thermalprinter/commits?author=%s", "@%s"),
    "issue": ("https://github.com/BoboTiG/thermalprinter/issues/%s", "issue #%s"),
    "pull": ("https://github.com/BoboTiG/thermalprinter/pull/%s", "PR #%s"),
}
intersphinx_mapping = {
    "icalevents": ("https://icalevents.readthedocs.io/en/latest/", None),
    "pillow": ("https://pillow.readthedocs.io/en/latest/", None),
    "python": ("https://docs.python.org/3", None),
}
project = "ThermalPrinter"
author = thermalprinter.__author__
copyright = thermalprinter.__copyright__.splitlines()[1].removeprefix("Copyright (c) ").strip()  # noqa: A001
version = thermalprinter.__version__

master_doc = "index"

# -- Options for HTML output ----------------------------------------------

html_theme = "shibuya"
html_theme_options = {
    "accent_color": "orange",
    "globaltoc_expand_depth": 1,
    "toctree_titles_only": False,
}
html_favicon = "../icon.svg"
html_context = {
    "source_type": "github",
    "source_user": "BoboTiG",
    "source_repo": "thermalprinter",
    "source_docs_path": "/docs/source/",
    "source_version": "main",
}

htmlhelp_basename = "ThermalPrinterdoc"

# -- Options for LaTeX output ---------------------------------------------

latex_documents = [
    (
        master_doc,
        "ThermalPrinter.tex",
        "ThermalPrinter Documentation",
        author,
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "thermalprinter", "ThermalPrinter Documentation", [author], 1)]
man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "ThermalPrinter",
        "ThermalPrinter Documentation",
        author,
        "ThermalPrinter",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# -- Options for Epub output ----------------------------------------------

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

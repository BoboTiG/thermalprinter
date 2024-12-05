# ThermalPrinter documentation build configuration file, created by
# sphinx-quickstart on Tue Sep 27 11:49:38 2016.

# -- General configuration ------------------------------------------------

extensions = [
    "enum_tools.autoenum",
    "sphinx_copybutton",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]
myst_links_external_new_tab = True
templates_path = []
source_suffix = {".rst": "restructuredtext"}
master_doc = "index"
project = "ThermalPrinter"
author = "Mickaël Schoentgen"
copyright = f"2016-2024, {author}"  # noqa: A001
version = "0.3.0"
release = "latest"
language = "en"
exclude_patterns = []
pygments_style = "sphinx"
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

html_theme = "shibuya"
html_theme_options = {
    "accent_color": "mint",
    "globaltoc_expand_depth": 2,
    "nav_links": [
        {"title": "Recipes", "url": "https://github.com/BoboTiG/thermalprinter-recipes"},
        {"title": "GitHub", "url": "https://github.com/BoboTiG/thermalprinter"},
        {"title": "PyPI", "url": "https://pypi.org/project/thermalprinter/"},
    ],
}
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

# For external links to standard library
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

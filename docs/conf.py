# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import functools
import sys
from os.path import abspath, dirname, join


# Make sure we get the version of this copy of Gluepy
sys.path.insert(1, dirname(dirname(abspath(__file__))))
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(abspath(join(dirname(__file__), "_ext")))

# Use the module to GitHub url resolver, but import it after the _ext directoy
# it lives in has been added to sys.path.
import github_links  # NOQA

project = 'Gluepy'
copyright = '2024, Gluepy'
author = 'Marcus Lind'
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "1.1"
# The full version, including alpha/beta/rc tags.
try:
    from gluepy import VERSION
except ImportError:
    release = version
else:
    release = VERSION

next_version = "1.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "gluepydocs",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    'sphinx_rtd_theme',
]

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%B %d, %Y"

# templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = "default-role-error"

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "trac"


# Links to Python's docs should reference the most recent version of the 3.x
# branch, which is located at this URL.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# Python's docs don't change every week.
intersphinx_cache_limit = 90  # days


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = ['_static']
html_last_updated_fmt = "%b %d, %Y"
modindex_common_prefix = ["gluepy."]

linkcode_resolve = functools.partial(
    github_links.github_linkcode_resolve,
    version=version,
    next_version=next_version,
)
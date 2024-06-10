"""
Sphinx plugins for Gluepy documentation.
"""

from sphinx.util import logging
logger = logging.getLogger(__name__)

def setup(app):
    app.add_crossref_type(
        directivename="setting",
        rolename="setting",
        indextemplate="pair: %s; setting",
    )
